import requests
import logging

URL = 'https://api.ipify.org?format=json'

_LOGGER = logging.getLogger(__name__)


def get_ip():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()['ip']
    except requests.exceptions.RequestException as e:
        _LOGGER.warning('Error while fetching external ip, ErrNo: %s', e.errno)
        return None
