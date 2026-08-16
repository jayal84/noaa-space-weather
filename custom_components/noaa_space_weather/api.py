"""API client for NOAA Space Weather."""

import logging

import aiohttp
from swpclib import swpclib

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class NoaaSpaceWeatherApiClient:
    """API client."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session
        self.swpc = swpclib.Runner()

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        try:
            data = await self.swpc.get_standard()
            data["predicted_f107cm_flux_data"] = await self._async_get_json(
                "https://services.swpc.noaa.gov/json/predicted_f107cm_flux.json"
            )
        except Exception:
            data = {}

        return data

    async def _async_get_json(self, url: str):
        async with self._session.get(url) as response:
            response.raise_for_status()
            return await response.json()
