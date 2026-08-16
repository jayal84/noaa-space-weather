"""Camera platform for NOAA Space Weather image feeds."""

from __future__ import annotations

import asyncio
import io
import mimetypes
from dataclasses import dataclass
import re
import time

import aiohttp
from PIL import Image as PILImage
from homeassistant.components.camera import Camera
from homeassistant.components.camera import CameraEntityDescription
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import ATTRIBUTION
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import MANUFACTURER


@dataclass(frozen=True, kw_only=True)
class NoaaSpaceWeatherCameraEntityDescription(CameraEntityDescription):
    """Describes a NOAA animation camera."""

    image_url: str | None = None
    directory_url: str | None = None
    filename_pattern: str | None = None
    frame_duration_ms: int = 0
    max_frames: int | None = None
    content_type: str | None = None


CAMERA_TYPES = (
    NoaaSpaceWeatherCameraEntityDescription(
        key="ovation_north",
        name="Aurora Ovation North",
        image_url="https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg",
        content_type="image/jpeg",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="aurora_forecast_south",
        name="Aurora Forecast South",
        image_url="https://services.swpc.noaa.gov/images/aurora-forecast-southern-hemisphere.jpg",
        content_type="image/jpeg",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="swx_overview_large",
        name="SWX Overview Large",
        image_url="https://services.swpc.noaa.gov/images/swx-overview-large.gif",
        content_type="image/gif",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="swx_overview_small",
        name="SWX Overview Small",
        image_url="https://services.swpc.noaa.gov/images/swx-overview-small.gif",
        content_type="image/gif",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="geospace_1_day",
        name="Geospace 1 Day",
        image_url="https://services.swpc.noaa.gov/images/geospacegeospace_1_day.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="geospace_3_day",
        name="Geospace 3 Day",
        image_url="https://services.swpc.noaa.gov/images/geospacegeospace_3_day.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="geospace_7_day",
        name="Geospace 7 Day",
        image_url="https://services.swpc.noaa.gov/images/geospacegeospace_7_day.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="synoptic_map",
        name="Synoptic Map",
        image_url="https://services.swpc.noaa.gov/images/synoptic-map.jpg",
        content_type="image/jpeg",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="station_a_index",
        name="Station A Index",
        image_url="https://services.swpc.noaa.gov/images/station-a-index.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="station_k_index",
        name="Station K Index",
        image_url="https://services.swpc.noaa.gov/images/station-k-index.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="ace_mag_24_hour",
        name="ACE MAG 24 Hour",
        image_url="https://services.swpc.noaa.gov/images/ace-mag-24-hour.gif",
        content_type="image/gif",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="ace_swepam_24_hour",
        name="ACE SWEPAM 24 Hour",
        image_url="https://services.swpc.noaa.gov/images/ace-swepam-24-hour.gif",
        content_type="image/gif",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="ace_mag_swepam_24_hour",
        name="ACE MAG SWEPAM 24 Hour",
        image_url="https://services.swpc.noaa.gov/images/ace-mag-swepam-24-hour.gif",
        content_type="image/gif",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="ace_epam_24_hour",
        name="ACE EPAM 24 Hour",
        image_url="https://services.swpc.noaa.gov/images/ace-epam-24-hour.gif",
        content_type="image/gif",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="boulder_magnetometer",
        name="Boulder Magnetometer",
        image_url="https://services.swpc.noaa.gov/images/boulder-magnetometer.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="notifications_timeline",
        name="Notifications Timeline",
        image_url="https://services.swpc.noaa.gov/images/notifications-timeline.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="notifications_in_effect_timeline",
        name="Notifications In Effect Timeline",
        image_url="https://services.swpc.noaa.gov/images/notifications-in-effect-timeline.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="relativistic_electron_fluence",
        name="Relativistic Electron Fluence",
        image_url="https://services.swpc.noaa.gov/images/relativistic-electron-fluence.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="storm_corrections",
        name="Storm Corrections",
        image_url="https://services.swpc.noaa.gov/images/storm-corrections.png",
        content_type="image/png",
        frame_duration_ms=0,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="ccor1",
        name="CCOR1 Animation",
        directory_url="https://services.swpc.noaa.gov/images/animations/ccor1/",
        filename_pattern=r"^\d{8}_\d{4}_ccor1_1024by960\.jpg$",
        frame_duration_ms=150,
        max_frames=120,
    ),
    NoaaSpaceWeatherCameraEntityDescription(
        key="suvi_195",
        name="SUVI 195 Animation",
        directory_url="https://services.swpc.noaa.gov/images/animations/suvi/primary/195/",
        filename_pattern=r"^or_suvi-l2-ci195_.*\.png$",
        frame_duration_ms=120,
        max_frames=60,
    ),
)


async def async_setup_entry(hass, entry, async_add_entities: AddConfigEntryEntitiesCallback):
    """Set up NOAA Space Weather animation cameras."""
    session = async_get_clientsession(hass)
    async_add_entities(
        [
            NoaaSpaceWeatherStaticCamera(entry, session, description)
            if description.image_url
            else NoaaSpaceWeatherAnimationCamera(entry, session, description)
            for description in CAMERA_TYPES
        ]
    )


class NoaaSpaceWeatherStaticCamera(Camera):
    """NOAA Space Weather static camera entity."""

    def __init__(self, config_entry, session: aiohttp.ClientSession, entity_description):
        super().__init__()
        self.config_entry = config_entry
        self.entity_description = entity_description
        self._session = session
        self.content_type = entity_description.content_type or mimetypes.guess_type(
            entity_description.image_url or ""
        )[0] or "image/jpeg"

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
            "source_url": self.entity_description.image_url,
        }

    async def async_camera_image(self, width: int | None = None, height: int | None = None):
        del width, height
        async with self._session.get(self.entity_description.image_url) as response:
            response.raise_for_status()
            return await response.read()


class NoaaSpaceWeatherAnimationCamera(Camera):
    """NOAA Space Weather animation camera entity."""

    def __init__(self, config_entry, session: aiohttp.ClientSession, entity_description):
        super().__init__()
        self.config_entry = config_entry
        self.entity_description = entity_description
        self._session = session
        self._cached_image: bytes | None = None
        self._frame_urls: list[str] = []
        self._cache_expires_at = 0.0
        self.content_type = "image/gif"

    @property
    def unique_id(self):
        return f"{self.config_entry.entry_id}_{self.entity_description.key}_animation"

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
            "frame_count": len(self._frame_urls),
        }

    async def async_camera_image(self, width: int | None = None, height: int | None = None):
        del width, height

        if self._cached_image is not None and time.monotonic() < self._cache_expires_at:
            return self._cached_image

        frame_urls = await self._async_get_frame_urls()
        self._frame_urls = frame_urls
        self._cached_image = await self._async_build_gif(frame_urls)
        self._cache_expires_at = time.monotonic() + 600
        return self._cached_image

    async def _async_get_frame_urls(self) -> list[str]:
        async with self._session.get(self.entity_description.directory_url) as response:
            response.raise_for_status()
            html = await response.text()

        filenames = sorted(
            {
                match
                for match in re.findall(r'href="([^"]+)"', html)
                if re.search(self.entity_description.filename_pattern, match)
                and not match.endswith("latest.jpg")
                and not match.endswith("latest.png")
            }
        )
        if self.entity_description.max_frames and len(filenames) > self.entity_description.max_frames:
            filenames = filenames[-self.entity_description.max_frames :]
        return [self.entity_description.directory_url + filename for filename in filenames]

    async def _async_build_gif(self, frame_urls: list[str]) -> bytes:
        if not frame_urls:
            return b""

        frame_bytes = await asyncio.gather(*(self._async_fetch_frame(url) for url in frame_urls))

        def _build() -> bytes:
            frames = []
            for data in frame_bytes:
                with PILImage.open(io.BytesIO(data)) as frame:
                    frames.append(frame.convert("RGBA"))

            output = io.BytesIO()
            first_frame, *remaining_frames = frames
            first_frame.save(
                output,
                format="GIF",
                save_all=True,
                append_images=remaining_frames,
                duration=self.entity_description.frame_duration_ms,
                loop=0,
                optimize=True,
                disposal=2,
            )
            return output.getvalue()

        return await asyncio.to_thread(_build)

    async def _async_fetch_frame(self, url: str) -> bytes:
        async with self._session.get(url) as response:
            response.raise_for_status()
            return await response.read()
