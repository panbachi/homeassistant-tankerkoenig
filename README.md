# Tankerkoenig Component

[![Version](https://img.shields.io/badge/version-0.2.1-green.svg?style=for-the-badge)](#) [![mantained](https://img.shields.io/maintenance/yes/2019.svg?style=for-the-badge)](#)

[![maintainer](https://img.shields.io/badge/maintainer-Goran%20Zunic%20%40panbachi-blue.svg?style=for-the-badge)](https://www.panbachi.de)

## Installation
1. Install this component by copying the files to your `/custom_components/` folder
2. Add this to your `configuration.yaml` using the config options below example.
3. **You will need to restart for the component to start working**

```yaml
tankerkoenig:
  api_key: YOUR_API_KEY
  monitored_conditions:
    - e5
    - e10
    - diesel
    - state
  stations:
    - id: '11571341-3296-4f16-a363-28b8c188872c'
      name: 'Aral - Kölner_Str.'
      street: 'Kölner Straße'
      brand: ARAL

```

### Options
| key                    | default                   | required | description
|------------------------|---------------------------|----------|---
| `api_key`              |                           | yes      | The API_KEY from Tankerkönig (descibed below)
| `monitored_conditions` | [e5, e10, diesel, state] | no       | What should be monitored

#### Stations
| key      | default           | required | description
|----------|-------------------|----------|---
| `id`     |                   | yes      | The ID of the station (descibed below)
| `name`   | tankerkoenig_[ID] | no       | Custom name of the station, used for the sensors
| `street` |                   | no       | Street of the station 
| `brand`  |                   | no       | Brand of the station

## Description
To create the API-KEY and find the IDs of the stations follow the first steps of the blog-post: 
https://www.panbachi.de/tankerkoenig-preise-in-home-assistant-darstellen-141/

The component will create three sensors and one binary_sensor for each station:

- `sensor.NAME_e5`
- `sensor.NAME_e10`
- `sensor.NAME_diesel`
- `binary_sensor.NAME_state`

The sensors are used for the price and the binary_sensor is used for the state if the station is currently open or not
and additionally stores the street and brand (if they were set).

***

Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding 
this, to resolve it, restart Home-Assistant.

***

# Support me / Follow me
[![Web](https://img.shields.io/badge/www-panbachi.de-blue.svg?style=flat-square&colorB=3d72a8&colorA=333333)](https://www.panbachi.de)
[![Facebook](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=facebook&colorB=3B5998&colorA=eee)](https://www.facebook.com/panbachi.de/)
[![Twitter](https://img.shields.io/badge/-%40panbachi-blue.svg?style=flat-square&logo=twitter&colorB=1DA1F2&colorA=eee)](https://twitter.com/panbachi)
[![Instagram](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=instagram&colorB=E4405F&colorA=eee)](http://instagram.com/panbachi.de)
[![YouTube](https://img.shields.io/badge/-%40panbachi-blue.svg?style=flat-square&logo=youtube&colorB=FF0000&colorA=eee)](https://www.youtube.com/channel/UCO7f2L7ZsDCpOtRfKnPqNow)
