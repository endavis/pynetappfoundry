"""Cache management CLI commands."""

import click

from pynetappfoundry.cli.commands.cache.aiqum import aiqum
from pynetappfoundry.cli.commands.cache.check import check
from pynetappfoundry.cli.commands.cache.clear import clear
from pynetappfoundry.cli.commands.cache.compliance import compliance
from pynetappfoundry.cli.commands.cache.history import history
from pynetappfoundry.cli.commands.cache.inspect import inspect
from pynetappfoundry.cli.commands.cache.occm import occm
from pynetappfoundry.cli.commands.cache.query import query
from pynetappfoundry.cli.commands.cache.refresh import refresh
from pynetappfoundry.cli.commands.cache.schema import schema
from pynetappfoundry.cli.commands.cache.show import show
from pynetappfoundry.cli.commands.cache.status import status


@click.group()
def cache() -> None:
    """Cluster metadata cache management.

    Commands for managing the local cache of cluster metadata.
    The cache stores discoverable ONTAP cluster information that
    doesn't change frequently.

    Use 'nf cache refresh' to populate or update the cache.
    Use 'nf cache history' to view change tracking.
    Use 'nf cache aiqum ...' for the AIQUM cache.
    """
    pass


cache.add_command(aiqum)
cache.add_command(check)
cache.add_command(clear)
cache.add_command(compliance)
cache.add_command(history)
cache.add_command(inspect)
cache.add_command(occm)
cache.add_command(query)
cache.add_command(refresh)
cache.add_command(schema)
cache.add_command(show)
cache.add_command(status)
