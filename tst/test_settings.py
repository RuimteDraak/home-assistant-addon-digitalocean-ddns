from src.app.settings import Settings


def test_ctor_none_string():
    settings = Settings(None)

    assert settings._settings == {}


def test_ctor_empty_string():
    settings = Settings('')

    assert settings._settings == {}


def test_ctor_empty_json_object():
    settings = Settings('{}')

    assert settings._settings == {}


def test_token_returns_string():
    settings = Settings('{"api_token": "test_token"}')

    assert settings.token == 'test_token'


def test_token_not_available_returns_none():
    settings = Settings('{}')

    assert settings.token is None


def test_domain_name_returns_string():
    settings = Settings('{"domain_name": "my_domain"}')

    assert settings.domain_name == 'my_domain'


def test_domain_name_not_available_returns_none():
    settings = Settings('{}')

    assert settings.domain_name is None


def test_domain_record_name_returns_string():
    settings = Settings('{"domain_record_name":"test.com"}')

    assert settings.domain_record_name == 'test.com'


def test_domain_record_name_not_available_returns_none():
    settings = Settings("{}")

    assert settings.domain_record_name is None

