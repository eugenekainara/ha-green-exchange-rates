"""Green Exchange Rates integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change

from .const import DOMAIN
from .coordinator import GreenExchangeRatesCoordinator

_LOGGER = logging.getLogger(__name__)

DEFAULT_INTERVAL_MINUTES = 60
DEFAULT_START_HOUR = 8
DEFAULT_END_HOUR = 20


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up integration from YAML (not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Green Exchange Rates from a config entry."""
    coordinator = GreenExchangeRatesCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    interval = entry.options.get("interval_minutes", DEFAULT_INTERVAL_MINUTES)
    start_hour = entry.options.get("start_hour", DEFAULT_START_HOUR)
    end_hour = entry.options.get("end_hour", DEFAULT_END_HOUR)

    async def _refresh_on_schedule(now):
        if start_hour <= now.hour <= end_hour and now.minute % interval == 0:
            await coordinator.async_request_refresh()

    cancel_listener = async_track_time_change(
        hass,
        _refresh_on_schedule,
        hour=list(range(start_hour, end_hour + 1)),
        minute=list(range(0, 60, interval)),
        second=0,
    )
    entry.async_on_unload(cancel_listener)
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload integration when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
