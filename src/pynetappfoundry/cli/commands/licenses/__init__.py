"""License management commands."""

import click

from pynetappfoundry.cli.commands.licenses.check import check
from pynetappfoundry.cli.commands.licenses.get import get
from pynetappfoundry.cli.commands.licenses.savings import savings


@click.group()
def licenses() -> None:
    """License management commands."""
    pass


licenses.add_command(check)
licenses.add_command(get)
licenses.add_command(savings)
