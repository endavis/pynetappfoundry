"""Utility commands."""

import click

from pynetappfoundry.cli.commands.utils.validate import validate
from pynetappfoundry.cli.commands.utils.run_cmd import run_cmd
from pynetappfoundry.cli.commands.utils.sqlite_to_excel import sqlite_to_excel


@click.group()
def utils() -> None:
    """Utility commands."""
    pass


utils.add_command(validate)
utils.add_command(run_cmd)
utils.add_command(sqlite_to_excel)
