# Janeiro - Configuration Management

- [Define configuration options](#define-configuration-options)
- [Select configuration source](#select-configuration-source)
  - [Python dictionnary](#python-dictionnary)
  - [Environment variables](#environment-variables)

## Define configuration options

In your application, you should declare options coming from configuration.

```python
DATABASE_MAX_CONNECTIONS_OPTION = ConfigOption(
    key="database.max_connections",
    type=int
)
```

Then whenever needed, you can load values for these options from config using:

```
max_connections = config.get(DATABASE_MAX_CONNECTIONS_OPTION)
```

**Read following sections to understand how to make your own Config object**

## Select configuration source

### Python dictionnary

**DictConfigSource** is the most simple configuration source. It loads config options from the python dictionnary it takes as a parameter.

```python
from janeiro.config import Config, DictConfigSource

config = Config(
    source=DictConfigSource({
        "database.url": "sqlite:///mydb.sqlite",
        "database.max_connections": "5"
    })
)
```

### Environment variables

**EnvConfigSource** loads config options from environment variables. It takes an optional prefix that can be used to prepend app name to all variables.

```python
from janeiro.config import Config, EnvConfigSource

config = Config(source=EnvConfigSource(prefix="app"))
```

With this configuration, accessing config option with key `database.max_connections` would read value from environment variable `APP_DATABASE_MAX_CONNECTIONS`.
