from unittest import mock

from janeiro.config import Config, DictConfigSource
from janeiro.database import (
    DATABASE_MIGRATIONS_PATH_OPTION,
    DATABASE_URL_OPTION,
    Database,
)


def test_database_config_factory_with_custom_config():
    config = Config(
        DictConfigSource(
            {
                DATABASE_URL_OPTION.key: "fake://database.url",
                DATABASE_MIGRATIONS_PATH_OPTION.key: "migrations/path",
            }
        )
    )
    with mock.patch("janeiro.database.Database") as db_initializer:
        Database.from_config(config)
        db_initializer.assert_called_once_with("fake://database.url", "migrations/path")


def test_database_config_factory_default_values():
    config = Config(DictConfigSource({}))
    with mock.patch("janeiro.database.Database") as db_initializer:
        Database.from_config(config)
        db_initializer.assert_called_once_with(
            DATABASE_URL_OPTION.default, DATABASE_MIGRATIONS_PATH_OPTION.default
        )
