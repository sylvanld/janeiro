from janeiro.context import set_app_context

set_app_context(app_name="Janeiro")

from janeiro.config import CONF
from janeiro.logging import setup_logging

setup_logging(CONF)

from janeiro.cli import CLI
from janeiro.cli.database import DatabaseCLI

cli = CLI()

cli.include_cli("db", DatabaseCLI("models:db"))

cli.dispatch()
