"""Base entity for NOAA Space Weather."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import MANUFACTURER


class NoaaSpaceWeatherEntity(CoordinatorEntity):
    """NOAA Space Weather Entity"""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return the integration device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer=MANUFACTURER,
        )
