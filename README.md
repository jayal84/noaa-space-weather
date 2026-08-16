# NOAA Space Weather

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

A non-official Home Assistant integration for the NOAA Space Weather Prediction Center API and imagery.

_Neither this integration nor its developer have any affiliation with NOAA._

**This component sets up the following platforms.**

| Platform | Description |
| -------- | ----------- |
| `sensor` | NOAA Space Weather values, forecasts, and diagnostics. |
| `camera` | NOAA Space Weather still images and animated image feeds. |

**Available sensors**

Core space weather values:

- `sensor.ssn` - Current sunspot number.
- `sensor.solar_flux_index` - Current solar flux index.
- `sensor.planetary_k_index` - Current planetary K-index.
- `sensor.a_index` - Predicted A-index.
- `sensor.a_index_2_day` - Predicted 2-day A-index.
- `sensor.a_index_3_day` - Predicted 3-day A-index.
- `sensor.polar_cap_absorption` - Polar cap absorption estimate.

Flare and particle probabilities:

- `sensor.c_class_1_day_probability`
- `sensor.c_class_2_day_probability`
- `sensor.c_class_3_day_probability`
- `sensor.m_class_1_day_probability`
- `sensor.m_class_2_day_probability`
- `sensor.m_class_3_day_probability`
- `sensor.x_class_1_day_probability`
- `sensor.x_class_2_day_probability`
- `sensor.x_class_3_day_probability`
- `sensor.proton_10mev_1_day_probability`
- `sensor.proton_10mev_2_day_probability`
- `sensor.proton_10mev_3_day_probability`

Flux, geomagnetic, and forecast diagnostics:

- `sensor.predicted_f107cm_1_day`
- `sensor.predicted_f107cm_2_day`
- `sensor.predicted_f107cm_3_day`
- `sensor.observed_f107cm_flux`
- `sensor.planetary_kp_estimated`
- `sensor.boulder_k_index`
- `sensor.forecast_ap`
- `sensor.forecast_f107`
- `sensor.planetary_kp_forecast`
- `sensor.f107_30_day_forecast`
- `sensor.kyoto_dst_index`

NOAA alerts and scales:

- `sensor.alerts_count`
- `sensor.latest_alert_code`
- `sensor.noaa_g_scale`
- `sensor.noaa_r_scale_minor_prob`
- `sensor.noaa_r_scale_major_prob`
- `sensor.noaa_s_scale_prob`

Solar cycle ranges:

- `sensor.solar_cycle_f107_range`
- `sensor.solar_cycle_ssn_range`

**Available cameras**

Static NOAA image feeds:

- `camera.ovation_north` - Aurora ovation north latest image.
- `camera.aurora_forecast_south` - Aurora forecast southern hemisphere image.
- `camera.swx_overview_large` - SWX overview large image.
- `camera.swx_overview_small` - SWX overview small image.
- `camera.geospace_1_day` - Geospace 1 day image.
- `camera.geospace_3_day` - Geospace 3 day image.
- `camera.geospace_7_day` - Geospace 7 day image.
- `camera.synoptic_map` - Synoptic map image.
- `camera.station_a_index` - Station A index image.
- `camera.station_k_index` - Station K index image.
- `camera.ace_mag_24_hour` - ACE MAG 24 hour image.
- `camera.ace_swepam_24_hour` - ACE SWEPAM 24 hour image.
- `camera.ace_mag_swepam_24_hour` - ACE MAG SWEPAM 24 hour image.
- `camera.ace_epam_24_hour` - ACE EPAM 24 hour image.
- `camera.boulder_magnetometer` - Boulder magnetometer image.
- `camera.notifications_timeline` - Notifications timeline image.
- `camera.notifications_in_effect_timeline` - Notifications in effect timeline image.
- `camera.relativistic_electron_fluence` - Relativistic electron fluence image.
- `camera.storm_corrections` - Storm corrections image.

Animated NOAA image loops:

- `camera.ccor1` - CCOR1 animation built from the historical frame directory.
- `camera.suvi_195` - SUVI 195 animation built from the historical frame directory.

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `noaa_space_weather`.
4. Download _all_ the files from the `custom_components/noaa_space_weather/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant.
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "NOAA Space Weather".

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/noaa_space_weather/__init__.py
custom_components/noaa_space_weather/api.py
custom_components/noaa_space_weather/camera.py
custom_components/noaa_space_weather/config_flow.py
custom_components/noaa_space_weather/const.py
custom_components/noaa_space_weather/entity.py
custom_components/noaa_space_weather/manifest.json
custom_components/noaa_space_weather/sensor.py
custom_components/noaa_space_weather/translations/en.json
custom_components/noaa_space_weather/translations/fr.json
custom_components/noaa_space_weather/translations/nb.json
custom_components/noaa_space_weather/translations/sv.json
```

## Configuration is done in the UI

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[buymecoffee]: https://www.buymeacoffee.com/tcarwash
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/tcarwash/home-assistant_noaa-space-weather.svg?style=for-the-badge
[commits]: https://github.com/tcarwash/home-assistant_noaa-space-weather/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/tcarwash/home-assistant_noaa-space-weather.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40tcarwash-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/tcarwash/home-assistant_noaa-space-weather.svg?style=for-the-badge
[releases]: https://github.com/tcarwash/home-assistant_noaa-space-weather/releases
[user_profile]: https://github.com/tcarwash
