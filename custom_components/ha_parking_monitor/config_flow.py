"""Config flow for HA Parking Monitor integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HAParkingMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA Parking Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="HA Parking Monitor", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional("allowed_vrms", default=[]): list,
                vol.Optional("webhook_token", default="my_secure_token"): str,
                vol.Optional("history_size", default=10): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HAParkingMonitorOptionsFlow(config_entry)


class HAParkingMonitorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for HA Parking Monitor."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for the custom integration."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional("allowed_vrms", default=self.config_entry.options.get("allowed_vrms", [])): list,
                vol.Optional("webhook_token", default=self.config_entry.options.get("webhook_token", "my_secure_token")): str,
                vol.Optional("history_size", default=self.config_entry.options.get("history_size", 10)): int,
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
