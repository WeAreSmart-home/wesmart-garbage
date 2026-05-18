import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.storage import Store
from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN, STORAGE_KEY, STORAGE_VERSION, SIGNAL_UPDATE_GARBAGE

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the WeSmart Garbage integration."""
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)

    data = await store.async_load() or {"schedule": {}}

    schedule = data.get("schedule", {})
    for day in schedule:
        if isinstance(schedule[day], dict):
            schedule[day] = [schedule[day]]

    hass.data[DOMAIN] = {
        "store": store,
        "schedule": schedule,
    }

    async def update_schedule(call):
        """Update the garbage schedule with toggle support."""
        day = str(call.data.get("day"))
        waste_name = call.data.get("waste_type")
        icon = call.data.get("icon")

        if not day or not waste_name:
            return

        if day not in hass.data[DOMAIN]["schedule"]:
            hass.data[DOMAIN]["schedule"][day] = []

        current_day_list = hass.data[DOMAIN]["schedule"][day]
        exists_idx = next(
            (i for i, x in enumerate(current_day_list) if x["name"] == waste_name), -1
        )

        if exists_idx > -1:
            current_day_list.pop(exists_idx)
        else:
            current_day_list.append({"name": waste_name, "icon": icon})

        await store.async_save({"schedule": hass.data[DOMAIN]["schedule"]})
        async_dispatcher_send(hass, SIGNAL_UPDATE_GARBAGE)

    hass.services.async_register(DOMAIN, "update_schedule", update_schedule)

    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True
