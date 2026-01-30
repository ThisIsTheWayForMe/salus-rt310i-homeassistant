"""Climate platform for SALUS RT310i integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ATTR_CURRENT_TEMP,
    ATTR_TARGET_TEMP,
    ATTR_HEATING_ON,
    DEFAULT_MIN_TEMP,
    DEFAULT_MAX_TEMP,
    DEFAULT_TEMP_STEP,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SALUS RT310i climate platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    device_id = hass.data[DOMAIN][entry.entry_id]["device_id"]
    
    async_add_entities([SalusClimate(coordinator, api, device_id)])


class SalusClimate(CoordinatorEntity, ClimateEntity):
    """Representation of a SALUS RT310i thermostat."""

    _attr_has_entity_name = True
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.TURN_ON
    )
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]

    def __init__(self, coordinator, api, device_id):
        """Initialize the thermostat."""
        super().__init__(coordinator)
        self._api = api
        self._device_id = device_id
        
        self._attr_unique_id = f"salus_{device_id}"
        self._attr_name = f"RT310i {device_id}"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._attr_name,
            "manufacturer": "SALUS",
            "model": "RT310i",
        }

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if self.coordinator.data and ATTR_CURRENT_TEMP in self.coordinator.data:
            try:
                temp = self.coordinator.data[ATTR_CURRENT_TEMP]
                # Temperature might be in format "21.5" or similar
                return float(temp) if temp else None
            except (ValueError, TypeError):
                _LOGGER.warning("Invalid current temperature value: %s", temp)
                return None
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        if self.coordinator.data and ATTR_TARGET_TEMP in self.coordinator.data:
            try:
                temp = self.coordinator.data[ATTR_TARGET_TEMP]
                return float(temp) if temp else None
            except (ValueError, TypeError):
                _LOGGER.warning("Invalid target temperature value: %s", temp)
                return None
        return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        if self.coordinator.data and ATTR_HEATING_ON in self.coordinator.data:
            # The API returns "1" for on, "0" for off
            heating_on = str(self.coordinator.data.get(ATTR_HEATING_ON, "0"))
            return HVACMode.HEAT if heating_on == "1" else HVACMode.OFF
        return HVACMode.OFF

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        return DEFAULT_MIN_TEMP

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        return DEFAULT_MAX_TEMP

    @property
    def target_temperature_step(self) -> float:
        """Return the supported step of target temperature."""
        return DEFAULT_TEMP_STEP

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        await self._api.set_temperature(temperature)
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        mode = "heat" if hvac_mode == HVACMode.HEAT else "off"
        await self._api.set_hvac_mode(mode)
        await self.coordinator.async_request_refresh()
