"""
A component/platform which allows you to get fuel prices from tankerkoenig.

For more details about this component, please refer to the documentation at
https://github.com/panbachi/homeassistant-tankerkoenig
"""
import logging
from datetime import timedelta, datetime

import voluptuous as vol
import requests

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_STATE,
    ATTR_UNIT_OF_MEASUREMENT,

    CONF_API_KEY,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    CONF_SCAN_INTERVAL,

    EVENT_HOMEASSISTANT_START,

    STATE_OPEN,
    STATE_CLOSED
)
from homeassistant.helpers.event import track_time_interval

__version__ = '0.1.0'

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'tankerkoenig'

TANKERKOENIG_PLATFORMS = ['sensor', 'binary_sensor']

SCAN_INTERVAL = timedelta(minutes=10)

CONF_ID = 'id'
CONF_STATIONS = 'stations'
CONF_STATION_ID = 'id'
CONF_STATION_STREET = 'street'
CONF_STATION_BRAND = 'brand'
CONF_STATION_NAME = 'name'

SENSOR_TYPES = {
    'e5': ['E5', '°C'],
    'e10': ['E10', 'lx'],
    'diesel': ['Diesel', '%'],
    'state': ['State', None]
}

STATION_SCHEMA = vol.Schema({
    vol.Required(CONF_STATION_ID): cv.string,
    vol.Optional(CONF_STATION_NAME): cv.string,
    vol.Optional(CONF_STATION_STREET): cv.string,
    vol.Optional(CONF_STATION_BRAND): cv.string
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_API_KEY): cv.string,
        #vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,
        vol.Required(CONF_STATIONS): vol.All(cv.ensure_list, [STATION_SCHEMA]),
        vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SENSOR_TYPES)):
            vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    tankerkoenig_config = config[DOMAIN]

    hass.data[DOMAIN] = TankerkoenigAPI(tankerkoenig_config)


    load_platform(hass, 'sensor', DOMAIN, tankerkoenig_config, config)

    if('state' in tankerkoenig_config[CONF_MONITORED_CONDITIONS]):
        load_platform(hass, 'binary_sensor', DOMAIN, tankerkoenig_config, config)

    def update_records_interval(now):
        hass.data[DOMAIN].update()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, update_records_interval)
    hass.services.register(DOMAIN, 'update', update_records_interval)
    track_time_interval(hass, update_records_interval, SCAN_INTERVAL)

    return True


class TankerkoenigDevice(Entity):
    def __init__(self, hass, station, config):
        if ('name' not in station):
            station['name'] = 'tankerkoenig_' + station['id']

        self._name = station['name']
        self._station = station
        self._id = station['id']
        self._api = hass.data[DOMAIN]
        self._api.add_station(self._id)

    @property
    def name(self):
        return self._name

    @property
    def device_state_attributes(self):
        attr = {CONF_NAME: self._name, CONF_ID: self._id}
        return attr

    def api(self):
        return self._api

    def id(self):
        return self._id


class TankerkoenigAPI:
    def __init__(self, config):
        self._config = config
        self._stations = []
        self._data = {}

    def add_station(self, id):
        self._stations.append(id)

    def get_inputs(self, id, fuel_type):
        if (id in self._data):
            fuel_type = fuel_type.lower()
            if(fuel_type in self._data[id]):
                return self._data[id][fuel_type.lower()]

        return None

    def get_status(self, id):
        if (id in self._data):
            return self._data[id]['status'] == 'open'

        return None

    def update(self):
        api_req = 'https://creativecommons.tankerkoenig.de/json/prices.php'
        api_req += '?apikey=' + self._config.get(CONF_API_KEY)
        api_req += '&ids=' + ','.join(self._stations)
        response = requests.get(api_req)
        _LOGGER.debug('Tankerkoenig API request: ' + api_req)
        if (response.json()['ok'] == True):
            self._data = response.json()['prices']
        else:
            _LOGGER.error('Tankerkoenig: ' + response.json()['status'] + ': ' + response.json()['message'])
