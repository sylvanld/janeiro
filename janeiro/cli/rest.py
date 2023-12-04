from typing import TYPE_CHECKING

import click

from janeiro.lazy import LazyImportTarget

if TYPE_CHECKING:
    from janeiro.rest import RestAPI




class RestCLI(click.Group):
    lazy_api: LazyImportTarget["RestAPI"]

    def __init__(self, api_importable_ref: str):
        super().__init__()
        self.lazy_api = LazyImportTarget.from_ref(api_importable_ref)

        self.add_command(self._build_start_api_cmd(), "start")

    def _build_start_api_cmd(self):
        @click.command
        @click.option("--host", type=str, default="127.0.0.1")
        @click.option("--port", type=int, default=9000)
        def start_api_cmd(host: str, port: int):
            self.lazy_api.do_import().start(host, port)

        return start_api_cmd
