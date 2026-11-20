
"""Sensors for Green Exchange Rates."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import GreenExchangeRatesCoordinator

SENSORS = {
    "usd_buy": ("USD buy", "USD", "mdi:currency-usd"),
    "usd_sell": ("USD sell", "USD", "mdi:currency-usd"),
    "eur_buy": ("EUR buy", "EUR", "mdi:currency-eur"),
    "eur_sell": ("EUR sell", "EUR", "mdi:currency-eur"),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up exchange-rate sensors."""
    coordinator: GreenExchangeRatesCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GreenExchangeRatesSensor(coordinator, entry, key, *details)
        for key, details in SENSORS.items()
    )


class GreenExchangeRatesSensor(CoordinatorEntity, SensorEntity):
    """One exchange-rate sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "UAH"
    _attr_suggested_display_precision = 2
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator, entry, key, name, currency, icon):
        super().__init__(coordinator)
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_icon = icon
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Green Exchange Rates",
            manufacturer="Custom integration",
            model="Telegram exchange-rate parser",
        )

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.key)

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        return {
            "source_text": self.coordinator.data.get("source_text"),
            "source": "Telegram public channel preview",
        }
