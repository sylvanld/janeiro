# Janeiro - Configurable Logging

## Enable configurable logging

Before doing any logs in your application, call `setup_logging` function.

```python
from janeiro.logging import setup_logging

setup_logging(config)
```

## Configure logging

The following configuration options are available for logging.

| Key                 | Description                                                                                                   | Default |
| ------------------- | ------------------------------------------------------------------------------------------------------------- | ------- |
| logging.config_file | Path to the a yaml file defining logging config. (see: https://docs.python.org/3/library/logging.config.html) | null    |
