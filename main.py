from janeiro.context import set_app_context

set_app_context(app_name="Manila")

from janeiro.config import CONF
from janeiro.database import Database
import models

db = Database("sqlite:///db.sqlite", "db_migrations")
db.generate_revision("initial revision")
