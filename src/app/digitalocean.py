import logging
import requests
from requests.exceptions import RequestException
from typing import List, Dict, Optional

_LOGGER = logging.getLogger(__name__)

API_BASE_URL = 'https://api.digitalocean.com/v2/'


class Api:
    def __init__(self, token):
        self._token = token

    def _base_headers(self):
        return {'Authorization': 'Bearer {:s}'.format(self._token)}

    def get_all_domains(self) -> List[Dict]:
        """Returns all managed domains."""
        headers = self._base_headers()

        try:
            result = requests.get(API_BASE_URL + 'domains', headers=headers)
            return result.json()['domains']
        except RequestException as e:
            _LOGGER.exception("Error fetching all domains")
            return []

    def get_domain(self, domain_name: str) -> Optional[Dict]:
        """Get the domain with the given name or None if it does not exist"""

        headers = self._base_headers()

        try:
            result = requests.get(API_BASE_URL + 'domains/' + domain_name + '/records', headers=headers)
            return result.json()['domain_records']
        except RequestException as e:
            _LOGGER.exception("Error fetching domain %s", domain_name)
            return None

    def create_domain(self, domain_name: str, record_name: str, ip: str) -> Optional[Dict]:
        """Create a new A domain record with the given name and ip address

            :returns the created domain if the operation was successful or None
        """

        headers = self._base_headers()
        body = {'type': 'A', 'name': record_name, 'data': ip}

        try:
            response = requests.post(API_BASE_URL + 'domains/' + domain_name + '/records',
                                     body,
                                     headers=headers)
            return response.json()['domain_record']
        except RequestException as e:
            _LOGGER.exception("Error creating domain entry")
            return None

    def update_domain(self, domain_name, record_id: int, ip: str):
        """Update an existing A domain record with the given name and ip address

           :returns the updated domain if the operation was successful or None
        """

        headers = self._base_headers()
        body = {'data': ip}

        try:
            response = requests.put(API_BASE_URL + 'domains/' + domain_name + '/records/' + str(record_id),
                                    body,
                                    headers=headers)
            return response.json()['domain_record']
        except RequestException as e:
            _LOGGER.exception("Error updating domain entry")
            return None
