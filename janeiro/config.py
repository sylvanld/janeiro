import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Generic, Type, TypeVar, Union

from janeiro.types import UNDEFINED

T = TypeVar("T")


@dataclass
class ConfigOption(Generic[T]):
    """Describes a config option of the application."""

    key: str
    type: Type[T]
    default: Any = UNDEFINED

    def has_default(self):
        """Check whether this option provides a default value."""
        if self.default != UNDEFINED:
            return True
        return False

    def get_default(self) -> Union[T, None]:
        """Get default value for this option."""
        if self.default != UNDEFINED:
            return self.default
        raise ValueError("No default value for config option: %s" % self.key)


class MissingConfigError(Exception):
    """Exception raised when a mandatory option is missing in config."""


class ConfigLoader:
    """Defines how string config is loaded into a proper python object."""

    def __init__(self, date_format: str = None):
        self.date_format = date_format or "%Y-%m-%d"

    def load(self, text: str, type: Type[T]) -> T:
        if type in (int, float, str):
            return type(text)
        elif type is bool:
            if text in ("yes", "true", "1"):
                return True
            elif text in ("no", "false", "0"):
                return False
            else:
                raise ValueError("Invalid value for boolean: %s" % text)
        elif type is Path:
            return Path(text)
        elif type is date:
            return datetime.strptime(text, self.date_format)
        raise TypeError("Unsupported type for deserializer: %s" % type)


class ConfigSource(ABC):
    """Defines how configuration is read from a given source."""

    @abstractmethod
    def get(self, key: str) -> str:
        raise NotImplementedError


class DictConfigSource(ConfigSource):
    def __init__(self, data: Dict[str, str]):
        self.data = data

    def get(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise MissingConfigError("Key is not defined in config: %s" % key)


class EnvConfigSource(ConfigSource):
    """Defines how configuration is read from environment variables."""

    def __init__(self, prefix: str = None):
        super().__init__()
        self.prefix = prefix

    def get(self, key):
        if self.prefix:
            key = self.prefix + "." + key
        variable = key.upper().replace(".", "_")

        value = os.getenv(variable, UNDEFINED)
        if value is UNDEFINED:
            raise MissingConfigError("Missing environment variable: %s" % variable)
        return value


class Config:
    """Interface used to read application configuration."""

    def __init__(self, source: ConfigSource, loader: ConfigLoader = None):
        self.cache = {}
        self.source = source
        self.loader = loader or ConfigLoader()

    def get(self, option: ConfigOption[T]) -> T:
        if option.key not in self.cache:
            try:
                raw_value = self.source.get(option.key)
                self.cache[option.key] = self.loader.load(raw_value, option.type)
            except MissingConfigError as error:
                if not option.has_default():
                    raise error
                self.cache[option.key] = option.get_default()

        return self.cache.get(option.key)
