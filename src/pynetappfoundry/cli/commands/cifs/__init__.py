"""CIFS commands."""

import click

from pynetappfoundry.cli.commands.cifs.session import session


@click.group()
def cifs() -> None:
    """CIFS / SMB inspection commands."""
    pass


cifs.add_command(session)
