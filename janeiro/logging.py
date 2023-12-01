import logging.config
from pathlib import Path

import yaml

from janeiro.config import Config, ConfigOption

LOGGING_CONFIG_FILE_OPTION = ConfigOption(
    key="logging.config_file", type=Path, default=None
)

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"standard": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter"}},
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"handlers": ["default"], "level": "DEBUG", "propagate": False},
}


def get_logging_config(config: Config):
    """Get logging config from logging.config_file config option.

    If not logging config file is specified, returns default logging config.
    """
    config_file_path = config.get(LOGGING_CONFIG_FILE_OPTION)
    if config_file_path is None:
        return DEFAULT_LOGGING_CONFIG

    if not config_file_path.exists():
        raise FileNotFoundError(
            "Logging config file %s does not exists" % config_file_path
        )

    with open(config_file_path, "r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)


def setup_logging(config: Config):
    """Setup logging according to config."""
    logging_config = get_logging_config(config)
    logging.config.dictConfig(logging_config)
