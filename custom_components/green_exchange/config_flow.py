"""Config and options flows for Green Exchange."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_CHANNEL, DEFAULT_CHANNEL, DOMAIN

DEFAULT_INTERVAL_MINUTES = 60
DEFAULT_START_HOUR = 8
DEFAULT_END_HOUR = 20

# These values divide an hour evenly, so refreshes occur on predictable
# minute boundaries (e.g. every 15 minutes at :00, :15, :30, :45).
INTERVAL_OPTIONS = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]


class GreenExchangeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle initial configuration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Configure the Telegram channel."""
        if user_input is not None:
            channel = user_input[CONF_CHANNEL].strip().lstrip("@")
            if not channel:
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required(CONF_CHANNEL, default=DEFAULT_CHANNEL): str,
                    }),
                    errors={"base": "invalid_channel"},
                )
            await self.async_set_unique_id(channel.lower())
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Green Exchange ({channel})",
                data={CONF_CHANNEL: channel},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_CHANNEL, default=DEFAULT_CHANNEL): str,
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow."""
        return GreenExchangeOptionsFlow(config_entry)


class GreenExchangeOptionsFlow(config_entries.OptionsFlow):
    """Configure polling interval and active hours."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage polling options."""
        if user_input is not None:
            if user_input["start_hour"] > user_input["end_hour"]:
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._get_schema(),
                    errors={"base": "invalid_hours"},
                )
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=self._get_schema())

    def _get_schema(self):
        options = self.config_entry.options
        return vol.Schema({
            vol.Required(
                "interval_minutes",
                default=options.get("interval_minutes", DEFAULT_INTERVAL_MINUTES),
            ): vol.In(INTERVAL_OPTIONS),
            vol.Required(
                "start_hour",
                default=options.get("start_hour", DEFAULT_START_HOUR),
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
            vol.Required(
                "end_hour",
                default=options.get("end_hour", DEFAULT_END_HOUR),
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
        })
