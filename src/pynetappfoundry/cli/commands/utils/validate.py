"""Validate cluster connectivity and configuration."""

from __future__ import annotations

import logging
import traceback
from typing import Any

import click
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster, Node, Volume

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_error, print_info, print_success, print_warning
from pynetappfoundry.core.config import Config


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Validation failed")
def validate(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Validate cluster connectivity and configuration.

    Tests connection to each cluster and verifies that the
    configured name matches the actual cluster name.
    """
    total_nodes = 0
    total_volumes = 0

    for name, details in clusters.items():
        print_info(f"Validating {name}...")
        node_count, vol_count = _validate_cluster(name, details, config)
        total_nodes += node_count
        total_volumes += vol_count

    print_info(f"\nTotal nodes: {total_nodes}")
    print_info(f"Total volumes: {total_volumes}")


def _validate_cluster(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> tuple[int, int]:
    """Validate a single cluster."""
    user, enc = config.get_user("clusters", name)
    node_count = 0
    vol_count = 0

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=enc,
            verify=False,
        ):
            cluster = Cluster()
            cluster.get()

            nodes = list(Node.get_collection())
            node_count = len(nodes)

            volumes = list(Volume.get_collection())
            vol_count = len(volumes)

            print_success(f"  Config {name} connected successfully")

            cluster_name = cluster["name"]
            if cluster_name != name:
                print_warning(f"    Config name {name} does not match cluster name {cluster_name}")

    except Exception as e:
        print_error(f"  Could not connect to config {name}")
        logging.debug(traceback.format_exc())

    return node_count, vol_count
