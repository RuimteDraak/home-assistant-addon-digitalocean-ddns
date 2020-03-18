import logging

from app.ip import get_ip
from app.settings import Settings
from app.digitalocean import Api

_LOGGER = logging.getLogger(__name__)

SETTINGS_FILE = '/data/options.json'

def configure_logging():
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

def read_config_file():
    with open(SETTINGS_FILE, 'rt') as file:
        content = file.read()
        return content

def main():
    configure_logging()

    raw_settings = read_config_file()
    settings = Settings(raw_settings)

    api = Api(settings.token)

    domain = api.get_domain(settings.domain_name)

    ip = get_ip()

    to_update = None
    for entry in domain:
        if entry['type'] == 'A' and entry['name'] == settings.domain_record_name:
            to_update = entry

    if ip is None:
        return

    if to_update is None:
        result = api.create_domain(settings.domain_name, settings.domain_record_name, ip)
        _LOGGER.info('Created record for %s with value %s', settings.domain_record_name, ip)
    elif to_update['data'] != ip:
        result = api.update_domain(settings.domain_name, to_update['id'], ip)
        _LOGGER.info('Updated record for %s with value %s', settings.domain_record_name, ip)
    else:
        _LOGGER.info('Ip has not changed, no update needed.')


if __name__ == '__main__':
    main()
