from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import DOMAIN, DEFAULT_ICON, SIGNAL_UPDATE_GARBAGE


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the garbage sensor."""
    async_add_entities([WeSmartGarbageSensor()])


class WeSmartGarbageSensor(SensorEntity):
    """Sensor that shows today's collection with reactive properties."""

    _attr_name = "WeSmart Garbage Today"
    _attr_unique_id = "wesmart_garbage_today"

    async def async_added_to_hass(self):
        """Register callbacks when added to hass."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPDATE_GARBAGE, self.async_write_ha_state
            )
        )

    @property
    def native_value(self):
        """Calculate state dynamically from memory."""
        today = str(datetime.now().isoweekday())
        schedule = self.hass.data[DOMAIN].get("schedule", {})
        if today in schedule and schedule[today]:
            return ", ".join([x["name"] for x in schedule[today]])
        return "Nothing"

    @property
    def icon(self):
        """Calculate icon dynamically from the first scheduled item."""
        today = str(datetime.now().isoweekday())
        schedule = self.hass.data[DOMAIN].get("schedule", {})
        if today in schedule and schedule[today]:
            return schedule[today][0].get("icon", DEFAULT_ICON)
        return DEFAULT_ICON

    @property
    def extra_state_attributes(self):
        """Always return the latest schedule from memory."""
        return {"schedule": self.hass.data[DOMAIN].get("schedule", {})}
