import json


class Settings:

    def __init__(self, settings: str):
        if settings is None or settings == '':
            self._settings = {}
        else:
            self._settings = json.loads(settings)

    @property
    def token(self):
        return self._settings.get('api_token')

    @property
    def domain_name(self):
        return self._settings.get('domain_name')

    @property
    def domain_record_name(self):
        return self._settings.get('domain_record_name')
