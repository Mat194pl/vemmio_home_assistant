"""Vemmio integration for Home Assistant."""

from __future__ import annotations

from vemmio import Device as VemmioDevice, Vemmio, VemmioError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class VemmioDataUpdateCoordinator(DataUpdateCoordinator[VemmioDevice]):
    """Class to manage fetching Vemmio data from single endpoint."""

    config_entry: ConfigEntry
    device: VemmioDevice

    def __init__(
        self,
        hass: HomeAssistant,
        *,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        LOGGER.debug("Initialized Vemmio coordinator")
        LOGGER.debug("Host: %s", entry.data[CONF_HOST])

        session = async_get_clientsession(hass)
        self.vemmio = Vemmio(entry.data[CONF_HOST], session)

        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> VemmioDevice:
        """Fetch data from Vemmio."""

        LOGGER.debug(
            "[coordinator.py] Updating Vemmio data from host %s", self.vemmio.host
        )
        try:
            device = await self.vemmio.update()
        except VemmioError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

        LOGGER.debug("Vemmio data: %s", str(device))

        self.device = device
        return device
