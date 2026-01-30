"""SALUS API client for RT310i thermostat."""
from __future__ import annotations

import logging
from typing import Any
import hashlib

import aiohttp
import async_timeout

from .const import (
    URL_LOGIN,
    URL_GET_TOKEN,
    URL_GET_DATA,
    URL_SET_DATA,
)

_LOGGER = logging.getLogger(__name__)


class SalusAPI:
    """Interface to the SALUS cloud API."""

    def __init__(self, username: str, password: str, device_id: str) -> None:
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.device_id = device_id
        self.session: aiohttp.ClientSession | None = None
        self.token: str | None = None
        self._session_owner = False
        self._cookies: dict = {}

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._session_owner = True
        return self.session

    async def login(self) -> bool:
        """Authenticate with the SALUS API."""
        session = await self._get_session()
        
        # Create password hash (MD5 is used by SALUS)
        password_hash = hashlib.md5(self.password.encode()).hexdigest()
        
        payload = {
            "IDemail": self.username,
            "password": password_hash,
            "login": "Login",
        }
        
        try:
            async with async_timeout.timeout(10):
                async with session.post(
                    URL_LOGIN,
                    data=payload,
                    allow_redirects=False
                ) as response:
                    if response.status == 302:  # Redirect on successful login
                        # Store cookies for subsequent requests
                        for cookie in session.cookie_jar:
                            self._cookies[cookie.key] = cookie.value
                        
                        # Get token from control page
                        return await self._get_token()
                    else:
                        _LOGGER.error("Login failed with status: %s", response.status)
                        return False
        except Exception as err:
            _LOGGER.error("Error during login: %s", err)
            raise

    async def _get_token(self) -> bool:
        """Get session token from control page."""
        session = await self._get_session()
        
        payload = {
            "devId": self.device_id,
        }
        
        try:
            async with async_timeout.timeout(10):
                async with session.post(
                    URL_GET_TOKEN,
                    data=payload,
                ) as response:
                    response.raise_for_status()
                    content = await response.text()
                    
                    # Extract token from response (it's embedded in the HTML/JS)
                    # The token is typically in a variable or hidden field
                    # This is a simplified version - actual implementation may need HTML parsing
                    if "token" in content.lower():
                        # Token retrieval successful
                        self.token = "authenticated"  # Cookies handle auth
                        _LOGGER.debug("Successfully obtained token")
                        return True
                    else:
                        _LOGGER.error("Could not find token in response")
                        return False
        except Exception as err:
            _LOGGER.error("Error getting token: %s", err)
            raise

    async def get_device_data(self) -> dict[str, Any]:
        """Get device data from the SALUS API."""
        if not self.token:
            await self.login()
        
        session = await self._get_session()
        
        params = {
            "devId": self.device_id,
            "current": 1,  # Get current values
        }
        
        try:
            async with async_timeout.timeout(10):
                async with session.get(
                    URL_GET_DATA,
                    params=params,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    _LOGGER.debug("Device data received: %s", data)
                    return data
        except Exception as err:
            _LOGGER.error("Error getting device data: %s", err)
            # Try to re-authenticate once
            self.token = None
            await self.login()
            raise

    async def set_temperature(self, temperature: float) -> bool:
        """Set target temperature for the device."""
        if not self.token:
            await self.login()
        
        session = await self._get_session()
        
        payload = {
            "devId": self.device_id,
            "current_tempZ1_set": str(temperature),
            "tempUnit": "0",  # 0 = Celsius, 1 = Fahrenheit
        }
        
        try:
            async with async_timeout.timeout(10):
                async with session.post(
                    URL_SET_DATA,
                    data=payload,
                ) as response:
                    response.raise_for_status()
                    result = await response.text()
                    
                    _LOGGER.debug("Set temperature response: %s", result)
                    return "success" in result.lower() or response.status == 200
        except Exception as err:
            _LOGGER.error("Error setting temperature: %s", err)
            raise

    async def set_hvac_mode(self, mode: str) -> bool:
        """Set HVAC mode for the device."""
        if not self.token:
            await self.login()
        
        session = await self._get_session()
        
        # Mode mapping: 0 = Off, 1 = On (Auto/Heat)
        mode_value = "1" if mode in ["heat", "auto"] else "0"
        
        payload = {
            "devId": self.device_id,
            "auto": mode_value,
        }
        
        try:
            async with async_timeout.timeout(10):
                async with session.post(
                    URL_SET_DATA,
                    data=payload,
                ) as response:
                    response.raise_for_status()
                    result = await response.text()
                    
                    _LOGGER.debug("Set HVAC mode response: %s", result)
                    return "success" in result.lower() or response.status == 200
        except Exception as err:
            _LOGGER.error("Error setting HVAC mode: %s", err)
            raise

    async def close(self) -> None:
        """Close the session."""
        if self.session and self._session_owner:
            await self.session.close()
            self.session = None
