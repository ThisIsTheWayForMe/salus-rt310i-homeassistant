"""Schedule management for SALUS RT310i integration."""
from __future__ import annotations

import logging
from datetime import time
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Default schedule templates
SCHEDULE_TEMPLATES = {
    "comfort": {
        "name": "Comfort Schedule",
        "periods": {
            "weekday": [
                {"start": "06:00", "end": "08:00", "temp": 21},  # Morning
                {"start": "08:00", "end": "17:00", "temp": 18},  # Day (away)
                {"start": "17:00", "end": "22:00", "temp": 21},  # Evening
                {"start": "22:00", "end": "06:00", "temp": 17},  # Night
            ],
            "weekend": [
                {"start": "07:00", "end": "23:00", "temp": 21},  # Day
                {"start": "23:00", "end": "07:00", "temp": 17},  # Night
            ],
        },
    },
    "eco": {
        "name": "Eco Schedule",
        "periods": {
            "weekday": [
                {"start": "06:00", "end": "08:00", "temp": 19},  # Morning
                {"start": "08:00", "end": "17:00", "temp": 16},  # Day (away)
                {"start": "17:00", "end": "22:00", "temp": 19},  # Evening
                {"start": "22:00", "end": "06:00", "temp": 16},  # Night
            ],
            "weekend": [
                {"start": "07:00", "end": "23:00", "temp": 19},  # Day
                {"start": "23:00", "end": "07:00", "temp": 16},  # Night
            ],
        },
    },
    "working_from_home": {
        "name": "Work From Home",
        "periods": {
            "weekday": [
                {"start": "06:00", "end": "08:00", "temp": 21},  # Morning
                {"start": "08:00", "end": "12:00", "temp": 20},  # Work morning
                {"start": "12:00", "end": "13:00", "temp": 21},  # Lunch
                {"start": "13:00", "end": "17:00", "temp": 20},  # Work afternoon
                {"start": "17:00", "end": "22:00", "temp": 21},  # Evening
                {"start": "22:00", "end": "06:00", "temp": 17},  # Night
            ],
            "weekend": [
                {"start": "08:00", "end": "23:00", "temp": 21},  # Day
                {"start": "23:00", "end": "08:00", "temp": 17},  # Night
            ],
        },
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SALUS RT310i schedule platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    device_id = hass.data[DOMAIN][entry.entry_id]["device_id"]
    
    # Create schedule entities for each template
    entities = [
        SalusScheduleMaster(coordinator, api, device_id),
    ]
    
    # Add template schedule switches
    for template_id, template_data in SCHEDULE_TEMPLATES.items():
        entities.append(
            SalusScheduleTemplate(coordinator, device_id, template_id, template_data)
        )
    
    async_add_entities(entities)


class SalusScheduleMaster(CoordinatorEntity, SwitchEntity, RestoreEntity):
    """Master schedule control switch."""

    def __init__(self, coordinator, api, device_id):
        """Initialize the schedule master."""
        super().__init__(coordinator)
        self._api = api
        self._device_id = device_id
        self._attr_name = "Schedule Master"
        self._attr_unique_id = f"salus_{device_id}_schedule_master"
        self._attr_icon = "mdi:calendar-clock"
        self._is_on = False

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": f"SALUS RT310i {self._device_id}",
            "manufacturer": "SALUS",
            "model": "RT310i",
        }

    @property
    def is_on(self) -> bool:
        """Return true if schedule is enabled."""
        # Check API data for schedule status
        if self.coordinator.data:
            return self.coordinator.data.get("CH1scheduleOn") == "1"
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable schedule mode."""
        try:
            # This would call the SALUS API to enable schedule
            # For now, we'll track it locally
            self._is_on = True
            _LOGGER.info("Schedule enabled for device %s", self._device_id)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to enable schedule: %s", err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable schedule mode."""
        try:
            self._is_on = False
            _LOGGER.info("Schedule disabled for device %s", self._device_id)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to disable schedule: %s", err)

    async def async_added_to_hass(self) -> None:
        """Restore state when added to hass."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state == "on"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        return {
            "active_schedule": self._get_active_schedule(),
            "available_templates": list(SCHEDULE_TEMPLATES.keys()),
        }

    def _get_active_schedule(self) -> str | None:
        """Get the currently active schedule template."""
        # Check which template is active
        for template_id in SCHEDULE_TEMPLATES:
            entity_id = f"switch.salus_{self._device_id}_schedule_{template_id}"
            state = self.hass.states.get(entity_id)
            if state and state.state == "on":
                return template_id
        return None


class SalusScheduleTemplate(CoordinatorEntity, SwitchEntity, RestoreEntity):
    """Schedule template switch."""

    def __init__(self, coordinator, device_id, template_id, template_data):
        """Initialize the schedule template."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._template_id = template_id
        self._template_data = template_data
        self._attr_name = f"Schedule {template_data['name']}"
        self._attr_unique_id = f"salus_{device_id}_schedule_{template_id}"
        self._attr_icon = "mdi:calendar-text"
        self._is_on = False

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": f"SALUS RT310i {self._device_id}",
            "manufacturer": "SALUS",
            "model": "RT310i",
        }

    @property
    def is_on(self) -> bool:
        """Return true if this schedule template is active."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Activate this schedule template."""
        try:
            # Turn off other templates
            for template_id in SCHEDULE_TEMPLATES:
                if template_id != self._template_id:
                    entity_id = f"switch.salus_{self._device_id}_schedule_{template_id}"
                    await self.hass.services.async_call(
                        "switch", "turn_off", {"entity_id": entity_id}, blocking=False
                    )
            
            self._is_on = True
            _LOGGER.info("Activated schedule template: %s", self._template_id)
            
            # Enable the master schedule
            master_entity_id = f"switch.salus_{self._device_id}_schedule_master"
            await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": master_entity_id}, blocking=False
            )
            
            self.async_write_ha_state()
        except Exception as err:
            _LOGGER.error("Failed to activate schedule: %s", err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Deactivate this schedule template."""
        try:
            self._is_on = False
            _LOGGER.info("Deactivated schedule template: %s", self._template_id)
            self.async_write_ha_state()
        except Exception as err:
            _LOGGER.error("Failed to deactivate schedule: %s", err)

    async def async_added_to_hass(self) -> None:
        """Restore state when added to hass."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state == "on"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return schedule details as attributes."""
        return {
            "template_id": self._template_id,
            "weekday_periods": self._template_data["periods"]["weekday"],
            "weekend_periods": self._template_data["periods"]["weekend"],
            "total_periods": (
                len(self._template_data["periods"]["weekday"])
                + len(self._template_data["periods"]["weekend"])
            ),
        }
