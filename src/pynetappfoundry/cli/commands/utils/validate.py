"""Validate cluster connectivity and configuration."""

from __future__ import annotations

import contextlib
import logging
import traceback
from typing import Any

import click
import paramiko
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
    user, password = config.get_user("clusters", name)
    node_count = 0
    vol_count = 0
    success = False

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=password,
            verify=False,
        ):
            cluster = Cluster()
            cluster.get()

            nodes = list(Node.get_collection())
            node_count = len(nodes)

            volumes = list(Volume.get_collection())
            vol_count = len(volumes)

            print_success("  API: Connected successfully")
            success = True

            cluster_name = cluster["name"]
            if cluster_name != name:
                print_warning(f"    Config name {name} does not match cluster name {cluster_name}")

    except Exception:
        print_error(f"  API: Could not connect to config {name}")
        logging.debug(traceback.format_exc())

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
    user, password = config.get_user("clusters", name)

    # Skip if no IP configured
    if "ip" not in details:
        print_warning("  SSH: Skipped (no IP configured)")
        return None

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(
            details["ip"],
            username=user,
            password=password,
            timeout=10,
        )
        # Run a simple command to verify the connection works
        _stdin, stdout, _stderr = ssh.exec_command("version")
        stdout.read()  # Consume output
        ssh.close()
        print_success("  SSH: Connected successfully")
        return True
    except paramiko.AuthenticationException:
        print_error("  SSH: Authentication failed (check username/password)")
        logging.debug(traceback.format_exc())
        return False
    except paramiko.SSHException as e:
        print_error(f"  SSH: Connection failed ({e})")
        logging.debug(traceback.format_exc())
        return False
    except TimeoutError:
        print_error("  SSH: Connection timed out")
        logging.debug(traceback.format_exc())
        return False
    except Exception as e:
        print_error(f"  SSH: Failed ({e})")
        logging.debug(traceback.format_exc())
        return False
    finally:
        with contextlib.suppress(Exception):
            ssh.close()
