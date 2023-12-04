import logging
import os
from typing import Type, TypeVar

import sqlalchemy.orm as orm
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from janeiro.config import Config, ConfigOption
from janeiro.query import Paginated, Pagination

DATABASE_URL_OPTION = ConfigOption(
    key="database.url", type=str, default="sqlite:///janeiro.sqlite"
)

DATABASE_MIGRATIONS_PATH_OPTION = ConfigOption(
    key="database.migrations.path", type=str, default="db/migrations"
)


T = TypeVar("T", bound=BaseModel)
LOG = logging.getLogger(__name__)


class Entity(DeclarativeBase):
    """Base class that should be inherited by SQLAlchemy models that maps to a table."""


class Database:
    def __init__(self, database_url: str, migrations_path: str):
        self.migrations_path = migrations_path
        self.engine = create_engine(database_url)
        self.session = scoped_session(session_factory=sessionmaker(bind=self.engine))

    @staticmethod
    def from_config(config: Config):
        database_url = config.get(DATABASE_URL_OPTION)
        migrations_path = config.get(DATABASE_MIGRATIONS_PATH_OPTION)
        return Database(database_url, migrations_path)

    def create_all(self, force: bool = False):
        if force:
            self.drop_all()
        LOG.info("Creating database schemas")
        Entity.metadata.create_all(self.engine)

    def drop_all(self):
        LOG.info("Dropping database schemas")
        Entity.metadata.drop_all(self.engine)

    def generate_revision(self, message: str):
        import alembic.command
        import alembic.config

        # config_path = os.path.join(self.migrations_path, "alembic.ini")
        config = alembic.config.Config()
        config.set_main_option("script_location", self.migrations_path)
        alembic.command.revision(config, message=message, autogenerate=True)
    
    def upgrade_revision(self):
        import alembic.command
        import alembic.config
        import alembic.script

        config = alembic.config.Config()
        config.set_main_option("script_location", self.migrations_path)
        script = alembic.script.ScriptDirectory.from_config(config)
        revision = script.get_heads()
        alembic.command.upgrade(config, revision)


def paginate(
    sql_query: orm.Query, *, pagination: Pagination, model: Type[T]
) -> Paginated[T]:
    """Fetch results of an SQLAlchemy query according to specified pagination."""
    paginated = Paginated(page=pagination.page, limit=pagination.limit)
    entities = (
        sql_query.offset(pagination.page * pagination.limit)
        .limit(pagination.limit)
        .all()
    )
    for entity in entities:
        paginated.results.append(model.from_orm(entity))
    paginated.size = len(paginated.results)
    paginated.total = sql_query.count()
    return paginated
