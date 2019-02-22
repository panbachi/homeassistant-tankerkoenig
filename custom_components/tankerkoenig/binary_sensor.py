"""
A component/platform which allows you to get fuel prices from tankerkoenig.

For more details about this component, please refer to the documentation at
https://github.com/panbachi/homeassistant-tankerkoenig
"""
import logging
from datetime import timedelta

from . import TankerkoenigDevice, CONF_STATIONS
from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.const import CONF_NAME
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['tankerkoenig']

CONF_ID = 'id'
CONF_STREET = 'street'
CONF_BRAND = 'brand'

SCAN_INTERVAL = timedelta(seconds=5)


def setup_platform(hass, config, add_entities, discovery_info=None):
    tankerkoenig_config = discovery_info

    sensors = []

    for station in tankerkoenig_config[CONF_STATIONS]:
        sensors.append(TankerkoenigBinarySensor(hass, station, tankerkoenig_config))

    add_entities(sensors)


class TankerkoenigBinarySensor(TankerkoenigDevice, BinarySensorDevice):
    """Implement an Tankerkoenig binary_sensor for displaying stations status."""

    def __init__(self, hass, station_config, config):
        """Initialize the sensor."""
        super().__init__(hass, station_config, config)
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} State'.format(self._name)

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        """Return the device class."""
        return 'door'

    @property
    def device_state_attributes(self):
        attr = {CONF_NAME: self._name, CONF_ID: 'test'}

        if('street' in self._station):
            attr[CONF_STREET] = self._station['street']

        if ('brand' in self._station):
            attr[CONF_BRAND] = slugify(self._station['brand']).upper()

        return attr

    def update(self):
        """Fetch new status from API."""
        self._state = self._api.get_status(self._id)

