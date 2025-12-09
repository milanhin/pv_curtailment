import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfPower
from homeassistant import config_entries

from .coordinator import PvCurtailingCoordinator
from .const import DOMAIN, COORDINATOR, SERIAL_NUMBER

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up sensor from config entry"""
    pv_coordinator = hass.data[DOMAIN][COORDINATOR]

    async_add_entities([SetpointSensor(coordinator=pv_coordinator), InverterPowerSensor(coordinator=pv_coordinator)])
    _LOGGER.info("PV Curtailment sensors were added")

class SetpointSensor(CoordinatorEntity, SensorEntity): # pyright: ignore[reportIncompatibleVariableOverride]
    """Sensor to store and show power setpoint for inverter"""

    _attr_name = "PV setpoint"
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, coordinator: PvCurtailingCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator

        # Set unique ID
        hass = self.coordinator.hass
        serial_number = hass.data[DOMAIN][SERIAL_NUMBER]
        self._attr_unique_id = serial_number + "_setpoint_sensor"
    
    @property
    def native_value(self) -> float | None: # pyright: ignore[reportIncompatibleVariableOverride]
        """Return setpoint so it gets stored by HA in the sensor"""
        return self.coordinator.setpoint_W

class InverterPowerSensor(CoordinatorEntity, SensorEntity): # pyright: ignore[reportIncompatibleVariableOverride]
    """Sensor to store and show production power of inverter"""

    _attr_name = "Inverter power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, coordinator: PvCurtailingCoordinator) -> None:
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator

        # Set unique ID
        hass = self.coordinator.hass
        serial_number = hass.data[DOMAIN][SERIAL_NUMBER]
        self._attr_unique_id = serial_number + "_inverter_power_sensor"

    @property
    def native_value(self) -> float | None: # pyright: ignore[reportIncompatibleVariableOverride]
        """Return power of inverter so it gets storen by HA in the sensor"""
        return self.coordinator.W