
"""Data update coordinator."""
from __future__ import annotations

import logging

from aiohttp import ClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_CHANNEL, DOMAIN
from .parser import parse_latest_rates

_LOGGER = logging.getLogger(__name__)


class GreenExchangeCoordinator(DataUpdateCoordinator):
    """Fetch rates from Telegram public preview."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.channel = entry.data[CONF_CHANNEL]
        self.url = f"https://t.me/s/{self.channel}"
        self.session = async_get_clientsession(hass)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=None,  # Refresh is scheduled at 08:00–20:00 by __init__.py
        )

    async def _async_update_data(self):
        """Fetch and parse the latest post."""
        try:
            async with self.session.get(
                self.url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; HomeAssistant/GreenExchange)"},
                timeout=20,
            ) as response:
                response.raise_for_status()
                html = await response.text()
            return parse_latest_rates(html)
        except (ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"Could not retrieve exchange rates: {err}") from err
