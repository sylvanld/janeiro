from typing import TYPE_CHECKING

import click

from janeiro.lazy import LazyImportTarget

if TYPE_CHECKING:
    from janeiro.database import Database


class DatabaseCLI(click.Group):
    lazy_db: LazyImportTarget["Database"]

    def __init__(self, db_importable_ref: str):
        super().__init__()
        self.lazy_db = LazyImportTarget.from_ref(db_importable_ref)

        self.add_command(self._build_db_revision_cmd(), "revision")
        self.add_command(self._build_db_upgrade_cmd(), "upgrade")

    def _build_db_revision_cmd(self):
        @click.command
        def db_revision_cmd():
            message = input("Revision description: ")
            self.lazy_db.do_import().generate_revision(message)

        return db_revision_cmd

    def _build_db_upgrade_cmd(self):
        @click.command
        def db_upgrade_cmd():
            self.lazy_db.do_import().upgrade_revision()

        return db_upgrade_cmd
