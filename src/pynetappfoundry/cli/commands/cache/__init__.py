"""Cache management CLI commands."""

import click

from pynetappfoundry.cli.commands.cache.clear import clear
from pynetappfoundry.cli.commands.cache.refresh import refresh
from pynetappfoundry.cli.commands.cache.show import show
from pynetappfoundry.cli.commands.cache.status import status


@click.group()
def cache() -> None:
    """Cluster metadata cache management.

    Commands for managing the local cache of cluster metadata.
    The cache stores discoverable ONTAP cluster information that
    doesn't change frequently.

    Use 'nf cache refresh' to populate or update the cache.
    """
    pass


cache.add_command(clear)
cache.add_command(refresh)
cache.add_command(show)
cache.add_command(status)
