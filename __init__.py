import logging
import voluptuous as vol
from datetime import datetime
from homeassistant.components.webhook import async_register
from homeassistant.helpers import config_validation as cv

DOMAIN = "ha_parking_monitor"
_LOGGER = logging.getLogger(__name__)
WEBHOOK_ID = "ha_parking_monitor"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional("allowed_vrms", default=[]): vol.All(cv.ensure_list, [cv.string]),
                vol.Optional("webhook_token", default="my_secure_token"): cv.string,
                vol.Optional("history_size", default=10): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the HA Parking Monitor integration."""
    settings = config.get(DOMAIN, {})
    allowed_vrms = settings.get("allowed_vrms", [])
    webhook_token = settings.get("webhook_token", "my_secure_token")
    history_size = settings.get("history_size", 10)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {"history": {}, "parked_vehicles": {}}

    async def handle_webhook(hass, webhook_id, request):
        """Handle incoming webhook data from ANPR cameras with multiple formats."""
        try:
            data = await request.json()

            # Validate the security token
            token = data.get("token") or data.get("auth") or data.get("access_key")
            if token != webhook_token:
                _LOGGER.warning("Unauthorized ANPR request")
                return

            # Normalize different JSON formats
            camera_id = data.get("camera_id") or data.get("camera") or "unknown_camera"
            vrm = data.get("vrm") or data.get("plate") or data.get("number_plate") or "unknown"
            direction = data.get("direction") or data.get("movement") or "unknown"
            timestamp = data.get("timestamp") or data.get("time") or datetime.utcnow().isoformat()

            entity_vrm = f"sensor.ha_parking_monitor_{camera_id}_vrm"
            entity_direction = f"sensor.ha_parking_monitor_{camera_id}_direction"
            entity_timestamp = f"sensor.ha_parking_monitor_{camera_id}_timestamp"

            if vrm in allowed_vrms or not allowed_vrms:
                hass.states.async_set(entity_vrm, vrm)
                hass.states.async_set(entity_direction, direction)
                hass.states.async_set(entity_timestamp, timestamp)

                _LOGGER.info(f"HA Parking Monitor update from {camera_id}: {vrm} moving {direction} at {timestamp}")

                # Handle parking
                if direction == "static":
                    hass.data[DOMAIN]["parked_vehicles"][vrm] = timestamp
                elif vrm in hass.data[DOMAIN]["parked_vehicles"]:
                    del hass.data[DOMAIN]["parked_vehicles"][vrm]

                # Store history
                history = hass.data[DOMAIN]["history"].get(camera_id, [])
                history.insert(0, {"vrm": vrm, "direction": direction, "timestamp": timestamp})
                if len(history) > history_size:
                    history.pop()

                hass.data[DOMAIN]["history"][camera_id] = history
                hass.states.async_set(f"sensor.ha_parking_monitor_{camera_id}_history", str(history))
                hass.states.async_set("sensor.ha_parking_monitor_parked_vehicles", str(hass.data[DOMAIN]["parked_vehicles"]))

            else:
                _LOGGER.info(f"Ignored VRM {vrm}, not in allowed list")

        except Exception as e:
            _LOGGER.error(f"Error processing HA Parking Monitor webhook: {e}")

    async_register(hass, DOMAIN, WEBHOOK_ID, handle_webhook)

    return True
