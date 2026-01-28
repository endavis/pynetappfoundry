"""Configuration management commands."""

import click

from pynetappfoundry.cli.commands.config.show import show
from pynetappfoundry.cli.commands.config.validate import validate


@click.group()
def config() -> None:
    """Configuration management commands.

    Commands for viewing and validating pynetappfoundry configuration.
    """
    pass


config.add_command(show)
config.add_command(validate)
