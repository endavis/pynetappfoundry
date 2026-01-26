"""Report generation commands."""

import click

from pynetappfoundry.cli.commands.reports.space_usage import space_usage
from pynetappfoundry.cli.commands.reports.locks import locks
from pynetappfoundry.cli.commands.reports.html import html


@click.group()
def reports() -> None:
    """Report generation commands."""
    pass


reports.add_command(space_usage)
reports.add_command(locks)
reports.add_command(html)
