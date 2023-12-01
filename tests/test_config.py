import os

import pytest

from janeiro.config import (
    Config,
    ConfigOption,
    DictConfigSource,
    EnvConfigSource,
    MissingConfigError,
)

CONFIG_DATA = {"database.url": "sqlite:///mydb.sqlite", "database.max_connections": "5"}


@pytest.fixture(scope="function")
def dict_config():
    yield Config(source=DictConfigSource(CONFIG_DATA))


@pytest.fixture(scope="function")
def env_config():
    for key, value in CONFIG_DATA.items():
        variable = "TEST_" + key.upper().replace(".", "_")
        os.environ[variable] = value
    yield Config(source=EnvConfigSource(prefix="test"))


CONFIG_FIXTURES = ["dict_config", "env_config"]


@pytest.fixture(scope="function")
def config(request, config_type: str):
    yield request.getfixturevalue(config_type)


@pytest.mark.parametrize("config_type", CONFIG_FIXTURES)
def test_config_get_defined_option(config: Config):
    database_url_option = ConfigOption("database.url", type=str)
    value = config.get(database_url_option)


@pytest.mark.parametrize("config_type", CONFIG_FIXTURES)
def test_config_get_non_string_type(config: Config):
    database_url_option = ConfigOption("database.max_connections", type=int)
    max_connections = config.get(database_url_option)
    assert isinstance(max_connections, int)


@pytest.mark.parametrize("config_type", CONFIG_FIXTURES)
def test_config_get_undefined_option(config: Config):
    database_url_option = ConfigOption("foo.bar", type=str)
    with pytest.raises(MissingConfigError):
        config.get(database_url_option)


@pytest.mark.parametrize("config_type", CONFIG_FIXTURES)
def test_config_get_undefined_option_with_default(config: Config):
    default_value = "foo"
    database_url_option = ConfigOption("foo.bar", type=str, default=default_value)
    value = config.get(database_url_option)
    assert value == default_value
