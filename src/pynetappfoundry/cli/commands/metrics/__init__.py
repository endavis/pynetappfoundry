"""Metrics commands."""

import click

from pynetappfoundry.cli.commands.metrics.dump_dii import dump_dii


@click.group()
def metrics() -> None:
    """Metrics commands."""
    pass


metrics.add_command(dump_dii)
