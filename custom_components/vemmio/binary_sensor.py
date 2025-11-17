"""Support for Vemmio binary sensors."""

from __future__ import annotations

from vemmio import Capability

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import VemmioConfigEntry
from .const import LOGGER
from .coordinator import VemmioDataUpdateCoordinator
from .entity import VemmioEntity, async_setup_attribute_entities_binary_sensors


async def async_setup_entry(
    hass: HomeAssistant,
    entry: VemmioConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Vemmio switches based on a config entry."""
    coordinator = entry.runtime_data
    LOGGER.debug("Setting up Vemmio binary sensor for host %s", entry.data["host"])

    async_setup_attribute_entities_binary_sensors(
        hass, async_add_entities, coordinator, VemmioBinarySensor
    )


class VemmioBinarySensor(VemmioEntity, BinarySensorEntity):
    """Defines a Vemmio binary sensor."""

    _capability: Capability
    _coordinator: VemmioDataUpdateCoordinator

    def __init__(
        self, coordinator: VemmioDataUpdateCoordinator, capability: Capability
    ) -> None:
        """Initialize."""

        self._attr_device_class = BinarySensorDeviceClass.DOOR

        LOGGER.debug("Initializing Vemmio binary sensor")
        LOGGER.debug(str(coordinator.data))
        LOGGER.debug("Host: %s", coordinator.vemmio.host)

        super().__init__(coordinator=coordinator, capability=capability)
        self._attr_unique_id = f"binary_sensor_{capability.get_uuid_with_id()}"
        self._coordinator = coordinator

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get_input_state(
            self._capability.node_uuid, self._capability.id
        )

    async def async_update(self) -> None:
        """Update entity."""
        await self._coordinator.data.get_status()

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state."""
        return True
