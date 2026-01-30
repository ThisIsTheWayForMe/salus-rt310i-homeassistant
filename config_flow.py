"""Config flow for SALUS RT310i integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_DEVICE_ID
from .salus_api import SalusAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_DEVICE_ID): str,
    }
)


class SalusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SALUS RT310i."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                # Test the credentials
                api = SalusAPI(
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_DEVICE_ID],
                )
                
                login_success = await api.login()
                
                if login_success:
                    # Use device_id as unique_id
                    await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
                    self._abort_if_unique_id_configured()
                    
                    return self.async_create_entry(
                        title=f"SALUS RT310i ({user_input[CONF_DEVICE_ID]})",
                        data=user_input,
                    )
                else:
                    errors["base"] = "invalid_auth"
                    
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
