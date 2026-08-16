"""Camera platform for NOAA Space Weather image feeds."""

from __future__ import annotations

from dataclasses import dataclass

import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import ATTRIBUTION
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import MANUFACTURER


@dataclass(frozen=True, kw_only=True)
class NoaaSpaceWeatherCameraEntityDescription:
    """Describes a NOAA image camera."""

    key: str
    name: str
    image_url: str


CAMERA_TYPES = (
    NoaaSpaceWeatherCameraEntityDescription(
        key="ovation_north",
        name="Aurora Ovation North",
        image_url="https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg",
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="suvi_195",
        name="SUVI 195",
        image_url="https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
    ),
)


async def async_setup_entry(hass, entry, async_add_entities: AddConfigEntryEntitiesCallback):
    """Set up NOAA Space Weather cameras."""
    session = async_get_clientsession(hass)
    async_add_entities(
        [NoaaSpaceWeatherCamera(entry, session, description) for description in CAMERA_TYPES]
    )


class NoaaSpaceWeatherCamera(Camera):
    """NOAA Space Weather camera entity."""

    def __init__(self, config_entry, session: aiohttp.ClientSession, entity_description):
        super().__init__()
        self.config_entry = config_entry
        self.entity_description = entity_description
        self._session = session

    @property
    def unique_id(self):
        return f"{self.config_entry.entry_id}_{self.entity_description.key}"

    @property
    def name(self):
        return self.entity_description.name

    @property
    def available(self):
        return True

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer=MANUFACTURER,
        )

    @property
    def extra_state_attributes(self):
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }

    async def async_camera_image(self, width: int | None = None, height: int | None = None):
        del width, height
        async with self._session.get(self.entity_description.image_url) as response:
            response.raise_for_status()
            return await response.read()
