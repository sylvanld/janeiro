import click


class CLI:
    def __init__(self):
        self.cli = click.Group()

    def include_cli(self, namespace: str, cli: click.Group):
        self.cli.add_command(cli, name=namespace)

    def dispatch(self):
        self.cli.main()
