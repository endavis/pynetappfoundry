"""Validate cluster connectivity and configuration."""

from __future__ import annotations

from typing import Any

import click

import pynetappfoundry.cache.ontap.cluster.nodes.mapping  # register TypeMapping
import pynetappfoundry.cache.ontap.storage.volumes.mapping  # noqa: F401 - register TypeMapping
from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import (
    print_debug,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.clients.ontap.cli import ONTAPCLI
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.query import QuerySet


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--ssh/--no-ssh",
    default=False,
    help="Also validate SSH connectivity (default: disabled).",
)
@with_config("Validation failed")
def validate(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    ssh: bool,
) -> None:
    """Validate cluster connectivity and configuration.

    Tests connection to each cluster and verifies that the
    configured name matches the actual cluster name.

    Use --ssh to also validate SSH connectivity for CLI commands.
    """
    total_nodes = 0
    total_volumes = 0
    api_success = 0
    api_failed = 0
    ssh_success = 0
    ssh_failed = 0
    ssh_skipped = 0

    for name, details in clusters.items():
        print_info(f"Validating {name}...")
        node_count, vol_count, api_ok = _validate_cluster(name, details, config)
        total_nodes += node_count
        total_volumes += vol_count
        if api_ok:
            api_success += 1
        else:
            api_failed += 1

        if ssh:
            ssh_ok = _validate_ssh(name, details, config)
            if ssh_ok is None:
                ssh_skipped += 1
            elif ssh_ok:
                ssh_success += 1
            else:
                ssh_failed += 1

    print_info(f"\nTotal nodes: {total_nodes}")
    print_info(f"Total volumes: {total_volumes}")
    print_info(f"API: {api_success} connected, {api_failed} failed")
    if ssh:
        print_info(f"SSH: {ssh_success} connected, {ssh_failed} failed, {ssh_skipped} skipped")


def _validate_cluster(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> tuple[int, int, bool]:
    """Validate a single cluster via API.

    Returns:
        Tuple of (node_count, volume_count, success).
    """
    node_count = 0
    vol_count = 0
    success = False

    try:
        cluster_config = ClusterConfig(**details)
        client = ONTAPAPIClient(cluster=cluster_config, config=config)

        response = client.call_endpoint("/cluster")
        cluster_name = response.get("name", "") if isinstance(response, dict) else ""

        node_count = QuerySet(OntapNodeResponse, client).count()
        vol_count = QuerySet(OntapVolume, client).count()

        print_success("  API: Connected successfully")
        success = True

        if cluster_name != name:
            print_warning(f"    Config name {name} does not match cluster name {cluster_name}")

    except Exception as e:
        print_error(f"  API: Could not connect to config {name}")
        print_debug(f"Exception details: {e}")

    return node_count, vol_count, success


def _validate_ssh(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> bool | None:
    """Validate SSH connectivity to a cluster.

    Returns:
        True if SSH connection succeeded, False if failed, None if skipped.
    """
    # Skip if no IP configured
    if "ip" not in details:
        print_warning("  SSH: Skipped (no IP configured)")
        return None

    user, password = config.get_user("clusters", name)
    cli = ONTAPCLI(name, details["ip"], user, password)

    try:
        cli.connect()
        cli.run_command("node show")
        cli.disconnect()
        print_success("  SSH: Connected successfully")
        return True
    except Exception as e:
        print_error(f"  SSH: Failed ({e})")
        print_debug(f"Exception details: {e}")
        return False
