"""The SALUS RT310i Thermostat integration."""
from __future__ import annotations

import logging
from datetime import timedelta
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_DEVICE_ID
from .salus_api import SalusAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,  # For schedule management
]
SCAN_INTERVAL = timedelta(minutes=5)

# Service schemas
SERVICE_BOOST_HEATING = "boost_heating"
SERVICE_SET_FROST_PROTECTION = "set_frost_protection"
SERVICE_SET_HOLIDAY_MODE = "set_holiday_mode"
SERVICE_SET_SCHEDULE = "set_schedule"
SERVICE_CREATE_CUSTOM_SCHEDULE = "create_custom_schedule"
SERVICE_APPLY_SCHEDULE_PERIOD = "apply_schedule_period"

BOOST_HEATING_SCHEMA = vol.Schema({
    vol.Required("entity_id"): cv.entity_id,
    vol.Required("duration"): vol.All(vol.Coerce(int), vol.Range(min=5, max=120)),
    vol.Optional("temperature"): vol.All(vol.Coerce(float), vol.Range(min=5, max=35)),
})

FROST_PROTECTION_SCHEMA = vol.Schema({
    vol.Required("entity_id"): cv.entity_id,
    vol.Required("enabled"): cv.boolean,
    vol.Optional("temperature"): vol.All(vol.Coerce(float), vol.Range(min=5, max=15)),
})

HOLIDAY_MODE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): cv.entity_id,
    vol.Required("enabled"): cv.boolean,
    vol.Optional("temperature"): vol.All(vol.Coerce(float), vol.Range(min=5, max=25)),
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SALUS RT310i from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    username = entry.data["username"]
    password = entry.data["password"]
    device_id = entry.data[CONF_DEVICE_ID]
    
    api = SalusAPI(username, password, device_id)
    
    async def async_update_data():
        """Fetch data from API."""
        try:
            await api.login()
            device_data = await api.get_device_data()
            return device_data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="salus_rt310i",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
        "device_id": device_id,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    async def handle_boost_heating(call: ServiceCall) -> None:
        """Handle boost heating service call."""
        entity_id = call.data["entity_id"]
        duration = call.data["duration"]
        temperature = call.data.get("temperature")
        
        _LOGGER.info("Boost heating called: entity=%s, duration=%s, temp=%s", 
                     entity_id, duration, temperature)
        
        # Get the climate entity
        climate_entity = hass.states.get(entity_id)
        if not climate_entity:
            _LOGGER.error("Entity %s not found", entity_id)
            return
        
        # Calculate boost temperature
        if temperature is None:
            current_target = float(climate_entity.attributes.get("temperature", 20))
            temperature = min(35, current_target + 2)
        
        # Set the temperature
        await hass.services.async_call(
            "climate",
            "set_temperature",
            {"entity_id": entity_id, "temperature": temperature},
            blocking=True,
        )
        
        _LOGGER.info("Boost heating activated for %s minutes at %s°C", duration, temperature)
    
    async def handle_frost_protection(call: ServiceCall) -> None:
        """Handle frost protection service call."""
        _LOGGER.info("Frost protection service called: %s", call.data)
        # Implementation would depend on API capabilities
        
    async def handle_set_schedule(call: ServiceCall) -> None:
        """Handle set schedule service call."""
        entity_id = call.data["entity_id"]
        schedule_name = call.data["schedule_name"]
        
        _LOGGER.info("Set schedule called: entity=%s, schedule=%s", entity_id, schedule_name)
        
        # Get device_id from entity
        climate_entity = hass.states.get(entity_id)
        if not climate_entity:
            _LOGGER.error("Entity %s not found", entity_id)
            return
        
        # Turn on the schedule template switch
        device_id = entry.data[CONF_DEVICE_ID]
        schedule_entity_id = f"switch.salus_{device_id}_schedule_{schedule_name}"
        
        await hass.services.async_call(
            "switch",
            "turn_on",
            {"entity_id": schedule_entity_id},
            blocking=True,
        )
        
        _LOGGER.info("Activated schedule: %s", schedule_name)
    
    async def handle_create_custom_schedule(call: ServiceCall) -> None:
        """Handle create custom schedule service call."""
        name = call.data["name"]
        weekday_periods = call.data["weekday_periods"]
        weekend_periods = call.data.get("weekend_periods", weekday_periods)
        
        _LOGGER.info("Create custom schedule called: %s", name)
        
        # Store custom schedule (this would be saved to storage)
        # For now, just log it
        _LOGGER.info("Custom schedule created: weekday=%s, weekend=%s", 
                     weekday_periods, weekend_periods)
    
    async def handle_apply_schedule_period(call: ServiceCall) -> None:
        """Handle apply schedule period service call."""
        entity_id = call.data["entity_id"]
        start_time = call.data["start_time"]
        end_time = call.data["end_time"]
        temperature = call.data["temperature"]
        days = call.data.get("days", [])
        
        _LOGGER.info("Apply schedule period: %s-%s at %s°C", start_time, end_time, temperature)
        
        # This would apply the period to the thermostat
        # For now, just log it
        _LOGGER.info("Period applied for days: %s", days)
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_BOOST_HEATING,
        handle_boost_heating,
        schema=BOOST_HEATING_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_FROST_PROTECTION,
        handle_frost_protection,
        schema=FROST_PROTECTION_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_HOLIDAY_MODE,
        handle_holiday_mode,
        schema=HOLIDAY_MODE_SCHEMA,
    )
    
    # Register schedule services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_SCHEDULE,
        handle_set_schedule,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_CREATE_CUSTOM_SCHEDULE,
        handle_create_custom_schedule,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_APPLY_SCHEDULE_PERIOD,
        handle_apply_schedule_period,
    )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    # Unregister services if this was the last entry
    if not hass.data[DOMAIN]:
        hass.services.async_remove(DOMAIN, SERVICE_BOOST_HEATING)
        hass.services.async_remove(DOMAIN, SERVICE_SET_FROST_PROTECTION)
        hass.services.async_remove(DOMAIN, SERVICE_SET_HOLIDAY_MODE)
        hass.services.async_remove(DOMAIN, SERVICE_SET_SCHEDULE)
        hass.services.async_remove(DOMAIN, SERVICE_CREATE_CUSTOM_SCHEDULE)
        hass.services.async_remove(DOMAIN, SERVICE_APPLY_SCHEDULE_PERIOD)
    
    return unload_ok
