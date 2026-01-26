"""Event management commands."""

import click

from pynetappfoundry.cli.commands.events.get import get
from pynetappfoundry.cli.commands.events.azevents import save_azure


@click.group()
def events() -> None:
    """Event management commands."""
    pass


events.add_command(get)
events.add_command(save_azure)
