"""Sensor platform for NOAA Space Weather."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .const import ICON
from .entity import NoaaSpaceWeatherEntity


def _first_record(coordinator, key: str) -> dict[str, Any]:
    data = coordinator.data.get(key)
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict):
        return data
    return {}


def _value_from(coordinator, source_key: str, value_key: str):
    record = _first_record(coordinator, source_key)
    return record.get(value_key)


def _percent_from(coordinator, source_key: str, value_key: str):
    value = _value_from(coordinator, source_key, value_key)
    return float(value) if value is not None else None


@dataclass(frozen=True, kw_only=True)
class NoaaSpaceWeatherSensorEntityDescription(SensorEntityDescription):
    """Describes NOAA Space Weather sensors."""

    value_fn: Callable[[Any], Any]


SENSOR_TYPES = (
    NoaaSpaceWeatherSensorEntityDescription(
        key="solar_flux_index",
        name="Solar Flux Index",
        icon="mdi:solar-power",
        native_unit_of_measurement="sfu",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(coordinator, "sfi_data", "sfi"),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="a_index",
        name="A Index",
        icon="mdi:compass-rose",
        native_unit_of_measurement="nT",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(coordinator, "a_index_data", "a_index"),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="a_index_2_day",
        name="A Index 2 Day",
        icon="mdi:compass-rose",
        native_unit_of_measurement="nT",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(
            coordinator, "a_index_data", "a_2_day_index"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="a_index_3_day",
        name="A Index 3 Day",
        icon="mdi:compass-rose",
        native_unit_of_measurement="nT",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(
            coordinator, "a_index_data", "a_3_day_index"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="planetary_k_index",
        name="Planetary K-Index",
        icon="mdi:alpha-k-box",
        native_unit_of_measurement="Kp",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(coordinator, "kp_index_data", "kp_index"),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="sunspot_number",
        name="Sunspot Number",
        icon="mdi:sun-wireless",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(coordinator, "ssn_data", "ssn"),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="polar_cap_absorption",
        name="Polar Cap Absorption",
        icon="mdi:sign-pole",
        value_fn=lambda coordinator: _value_from(
            coordinator, "probabilities_data", "polar_cap_absorption"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="c_class_1_day_probability",
        name="C-Class 1 Day Probability",
        icon="mdi:weather-sunny-alert",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "c_class_1_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="c_class_2_day_probability",
        name="C-Class 2 Day Probability",
        icon="mdi:weather-sunny-alert",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "c_class_2_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="c_class_3_day_probability",
        name="C-Class 3 Day Probability",
        icon="mdi:weather-sunny-alert",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "c_class_3_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="m_class_1_day_probability",
        name="M-Class 1 Day Probability",
        icon="mdi:sun-wireless-outline",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "m_class_1_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="m_class_2_day_probability",
        name="M-Class 2 Day Probability",
        icon="mdi:sun-wireless-outline",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "m_class_2_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="m_class_3_day_probability",
        name="M-Class 3 Day Probability",
        icon="mdi:sun-wireless-outline",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "m_class_3_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="x_class_1_day_probability",
        name="X-Class 1 Day Probability",
        icon="mdi:sun-wireless",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "x_class_1_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="x_class_2_day_probability",
        name="X-Class 2 Day Probability",
        icon="mdi:sun-wireless",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "x_class_2_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="x_class_3_day_probability",
        name="X-Class 3 Day Probability",
        icon="mdi:sun-wireless",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "x_class_3_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="proton_10mev_1_day_probability",
        name="10 MeV Proton 1 Day Probability",
        icon="mdi:radioactive",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "10mev_protons_1_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="proton_10mev_2_day_probability",
        name="10 MeV Proton 2 Day Probability",
        icon="mdi:radioactive",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "10mev_protons_2_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="proton_10mev_3_day_probability",
        name="10 MeV Proton 3 Day Probability",
        icon="mdi:radioactive",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _percent_from(
            coordinator, "probabilities_data", "10mev_protons_3_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="predicted_f107cm_1_day",
        name="Predicted 10.7 cm Flux 1 Day",
        icon="mdi:radio-tower",
        native_unit_of_measurement="sfu",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(
            coordinator, "predicted_f107cm_flux_data", "tencmfcst_1_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="predicted_f107cm_2_day",
        name="Predicted 10.7 cm Flux 2 Day",
        icon="mdi:radio-tower",
        native_unit_of_measurement="sfu",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(
            coordinator, "predicted_f107cm_flux_data", "tencmfcst_2_day"
        ),
    ),
    NoaaSpaceWeatherSensorEntityDescription(
        key="predicted_f107cm_3_day",
        name="Predicted 10.7 cm Flux 3 Day",
        icon="mdi:radio-tower",
        native_unit_of_measurement="sfu",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda coordinator: _value_from(
            coordinator, "predicted_f107cm_flux_data", "tencmfcst_3_day"
        ),
    ),
)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [NoaaSpaceWeatherSensor(coordinator, entry, description) for description in SENSOR_TYPES]
    )


class NoaaSpaceWeatherSensor(NoaaSpaceWeatherEntity, SensorEntity):
    """NOAA Space Weather sensor."""

    def __init__(self, coordinator, entry, entity_description):
        self.entity_description = entity_description
        super().__init__(coordinator, entry)

    @property
    def unique_id(self):
        return f"{self.config_entry.entry_id}_{self.entity_description.key}"

    @property
    def name(self):
        return self.entity_description.name

    @property
    def icon(self):
        return self.entity_description.icon or ICON

    @property
    def native_value(self):
        return self.entity_description.value_fn(self.coordinator)

    @property
    def native_unit_of_measurement(self):
        return self.entity_description.native_unit_of_measurement

    @property
    def state_class(self):
        return self.entity_description.state_class

    @property
    def available(self):
        return super().available and self.coordinator.data is not None
