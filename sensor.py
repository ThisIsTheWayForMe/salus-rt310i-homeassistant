"""Sensor platform for SALUS RT310i integration."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime, PERCENTAGE
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
    """Set up SALUS RT310i sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    device_id = hass.data[DOMAIN][entry.entry_id]["device_id"]
    
    sensors = [
        SalusTargetTemperatureSensor(coordinator, device_id),
        SalusHeatingDemandSensor(coordinator, device_id),
        SalusLastUpdateSensor(coordinator, device_id),
        SalusOperationModeSensor(coordinator, device_id),
    ]
    
    # Add optional sensors if data available
    if coordinator.data.get("CH1frostProtectionTemp"):
        sensors.append(SalusFrostProtectionSensor(coordinator, device_id))
    
    async_add_entities(sensors)


class SalusBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for SALUS sensors."""

    def __init__(self, coordinator, device_id, sensor_type: str, name: str):
        """Initialize the sensor."""
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


class SalusTargetTemperatureSensor(SalusBaseSensor):
    """Sensor for target temperature."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "target_temp", "Target Temperature")
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "°C"

    @property
    def native_value(self) -> float | None:
        """Return the target temperature."""
        if self.coordinator.data and "CH1currentSetPoint" in self.coordinator.data:
            try:
                return float(self.coordinator.data["CH1currentSetPoint"])
            except (ValueError, TypeError):
                return None
        return None


class SalusHeatingDemandSensor(SalusBaseSensor):
    """Sensor for heating demand percentage."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "heating_demand", "Heating Demand")
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_icon = "mdi:fire"

    @property
    def native_value(self) -> int | None:
        """Return the heating demand."""
        if self.coordinator.data:
            current_temp = self.coordinator.data.get("CH1currentRoomTemp")
            target_temp = self.coordinator.data.get("CH1currentSetPoint")
            heating_on = self.coordinator.data.get("CH1heatOnOff")
            
            if current_temp and target_temp and heating_on:
                try:
                    current = float(current_temp)
                    target = float(target_temp)
                    is_heating = heating_on == "1"
                    
                    if not is_heating:
                        return 0
                    
                    # Calculate demand based on temperature difference
                    diff = target - current
                    if diff <= 0:
                        return 0
                    
                    # Scale to percentage (max 5°C difference = 100%)
                    demand = min(100, int((diff / 5.0) * 100))
                    return demand
                except (ValueError, TypeError):
                    pass
        return 0


class SalusLastUpdateSensor(SalusBaseSensor):
    """Sensor for last update time."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "last_update", "Last Update")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> datetime | None:
        """Return the last update time."""
        if self.coordinator.last_update_success_time:
            return self.coordinator.last_update_success_time
        return None


class SalusOperationModeSensor(SalusBaseSensor):
    """Sensor for operation mode."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "operation_mode", "Operation Mode")
        self._attr_icon = "mdi:thermostat-auto"

    @property
    def native_value(self) -> str | None:
        """Return the operation mode."""
        if self.coordinator.data:
            heating_on = self.coordinator.data.get("CH1heatOnOff", "0")
            auto_off = self.coordinator.data.get("CH1autoOff", "0")
            schedule_on = self.coordinator.data.get("CH1scheduleOn", "0")
            
            if heating_on == "0":
                return "Off"
            elif schedule_on == "1":
                return "Schedule"
            elif auto_off == "0":
                return "Manual"
            else:
                return "Auto"
        return "Unknown"

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        if self.coordinator.data:
            return {
                "heating_enabled": self.coordinator.data.get("CH1heatOnOff") == "1",
                "schedule_enabled": self.coordinator.data.get("CH1scheduleOn") == "1",
                "auto_mode": self.coordinator.data.get("CH1autoOff") == "0",
            }
        return {}


class SalusFrostProtectionSensor(SalusBaseSensor):
    """Sensor for frost protection temperature."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, "frost_protection", "Frost Protection")
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "°C"
        self._attr_icon = "mdi:snowflake-alert"

    @property
    def native_value(self) -> float | None:
        """Return the frost protection temperature."""
        if self.coordinator.data and "CH1frostProtectionTemp" in self.coordinator.data:
            try:
                return float(self.coordinator.data["CH1frostProtectionTemp"])
            except (ValueError, TypeError):
                return None
        return None
