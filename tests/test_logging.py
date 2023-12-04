import json
from unittest import mock

from janeiro.config import Config, DictConfigSource
from janeiro.logging import DEFAULT_LOGGING_CONFIG, setup_logging


def test_setup_logging():
    with mock.patch("logging.config.dictConfig") as mock_dict_config:
        config = Config(DictConfigSource({}))
        setup_logging(config)
        mock_dict_config.assert_called_once_with(DEFAULT_LOGGING_CONFIG)


def test_setup_logging_with_config_file():
    logging_config = {"foo": "bar"}
    with open("/tmp/logging-config.json", "w") as logging_config_file:
        json.dump(logging_config, logging_config_file)

    with mock.patch("logging.config.dictConfig") as mock_dict_config:
        config = Config(
            DictConfigSource({"logging.config_file": "/tmp/logging-config.json"})
        )
        setup_logging(config)
        mock_dict_config.assert_called_once_with(logging_config)
