"""Binary sensor platform for SALUS RT310i integration."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SALUS RT310i binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    device_id = hass.data[DOMAIN][entry.entry_id]["device_id"]
    
    sensors = [
        SalusHeatingSensor(coordinator, device_id),
        SalusConnectionSensor(coordinator, device_id),
        SalusScheduleSensor(coordinator, device_id),
    ]
    
    # Add optional sensors
    if coordinator.data.get("holidayEnabled") is not None:
        sensors.append(SalusHolidayModeSensor(coordinator, device_id))
    
    if coordinator.data.get("CH1tempLowAlarmStatus") is not None:
        sensors.extend([
            SalusLowTempAlarmSensor(coordinator, device_id),
            SalusHighTempAlarmSensor(coordinator, device_id),
        ])
    
    async_add_entities(sensors)


class SalusBaseBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Base class for SALUS binary sensors."""

    def __init__(self, coordinator, device_id, sensor_type: str, name: str):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_unique_id = f"salus_{device_id}_{sensor_type}"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": f"SALUS RT310i {self._device_id}",
            "manufacturer": "SALUS",
            "model": "RT310i",
        }


class SalusHeatingSensor(SalusBaseBinarySensor):
    """Binary sensor for heating status."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "heating", "Heating")
        self._attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self) -> bool:
        """Return true if heating is active."""
        if self.coordinator.data:
            # Check both heating on and relay status
            heating_on = self.coordinator.data.get("CH1heatOnOff", "0")
            relay_on = self.coordinator.data.get("CH1heatOnOffStatus", "0")
            return heating_on == "1" and relay_on == "1"
        return False

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        if self.coordinator.data:
            current_temp = self.coordinator.data.get("CH1currentRoomTemp")
            target_temp = self.coordinator.data.get("CH1currentSetPoint")
            
            attrs = {
                "relay_status": self.coordinator.data.get("CH1heatOnOffStatus") == "1",
            }
            
            if current_temp and target_temp:
                try:
                    diff = float(target_temp) - float(current_temp)
                    attrs["temperature_difference"] = round(diff, 1)
                except (ValueError, TypeError):
                    pass
            
            return attrs
        return {}


class SalusConnectionSensor(SalusBaseBinarySensor):
    """Binary sensor for connection status."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "connection", "Connection")
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self) -> bool:
        """Return true if connected."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        attrs = {}
        if self.coordinator.last_update_success_time:
            attrs["last_success"] = self.coordinator.last_update_success_time.isoformat()
        if hasattr(self.coordinator, 'last_exception') and self.coordinator.last_exception:
            attrs["last_error"] = str(self.coordinator.last_exception)
        return attrs


class SalusScheduleSensor(SalusBaseBinarySensor):
    """Binary sensor for schedule status."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "schedule", "Schedule Active")
        self._attr_icon = "mdi:calendar-clock"

    @property
    def is_on(self) -> bool:
        """Return true if schedule is enabled."""
        if self.coordinator.data:
            return self.coordinator.data.get("CH1scheduleOn") == "1"
        return False

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        if self.coordinator.data:
            return {
                "program_mode": self.coordinator.data.get("progMode", "unknown"),
            }
        return {}


class SalusHolidayModeSensor(SalusBaseBinarySensor):
    """Binary sensor for holiday mode."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "holiday_mode", "Holiday Mode")
        self._attr_icon = "mdi:beach"

    @property
    def is_on(self) -> bool:
        """Return true if holiday mode is enabled."""
        if self.coordinator.data:
            return self.coordinator.data.get("holidayEnabled") == "1"
        return False


class SalusLowTempAlarmSensor(SalusBaseBinarySensor):
    """Binary sensor for low temperature alarm."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "low_temp_alarm", "Low Temperature Alarm")
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def is_on(self) -> bool:
        """Return true if low temperature alarm is active."""
        if self.coordinator.data:
            return self.coordinator.data.get("CH1tempLowAlarmStatus") == "1"
        return False


class SalusHighTempAlarmSensor(SalusBaseBinarySensor):
    """Binary sensor for high temperature alarm."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "high_temp_alarm", "High Temperature Alarm")
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def is_on(self) -> bool:
        """Return true if high temperature alarm is active."""
        if self.coordinator.data:
            return self.coordinator.data.get("CH1tempHighAlarmStatus") == "1"
        return False
