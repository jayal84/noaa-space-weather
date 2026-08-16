"""API client for NOAA Space Weather."""

from __future__ import annotations

import asyncio
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
            predicted_f107cm_flux_data, f107_cm_flux_data, planetary_k_index_1m_data, boulder_k_index_1m_data, forecast_45_day_data = await asyncio.gather(
                self._async_get_json(
                    "https://services.swpc.noaa.gov/json/predicted_f107cm_flux.json"
                ),
                self._async_get_json(
                    "https://services.swpc.noaa.gov/json/f107_cm_flux.json"
                ),
                self._async_get_json(
                    "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
                ),
                self._async_get_json(
                    "https://services.swpc.noaa.gov/json/boulder_k_index_1m.json"
                ),
                self._async_get_json(
                    "https://services.swpc.noaa.gov/json/45-day-forecast.json"
                ),
                return_exceptions=False,
            )
            data["predicted_f107cm_flux_data"] = predicted_f107cm_flux_data
            data["f107_cm_flux_data"] = f107_cm_flux_data
            data["planetary_k_index_1m_data"] = planetary_k_index_1m_data
            data["boulder_k_index_1m_data"] = boulder_k_index_1m_data
            data["forecast_45_day_data"] = forecast_45_day_data
        except Exception:
            data = {}

        return data

    async def _async_get_json(self, url: str):
        async with self._session.get(url) as response:
            response.raise_for_status()
            return await response.json()
