"""Run CLI commands on clusters."""

from __future__ import annotations

import logging
from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import console, print_error, print_info
from pynetappfoundry.clients.ontap.cli import ONTAPCLI
from pynetappfoundry.core.config import Config


@click.command("run-cmd")
@click.argument("command")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Run command failed")
def run_cmd(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    command: str,
) -> None:
    """Run CLI commands on clusters.

    Executes the given ONTAP CLI command on all matching clusters
    via SSH.

    Example: nf utils run-cmd "vol show"
    """
    for name, details in clusters.items():
        print_info(f"Running command on {name}...")
        _run_cluster_command(name, details, config, command)


def _run_cluster_command(
    name: str,
    details: dict[str, Any],
    config: Config,
    command: str,
) -> None:
    """Run command on a single cluster."""
    user, enc = config.get_user("clusters", name)

    try:
        cli = ONTAPCLI(
            name=name,
            host_or_ip=details["ip"],
            username=user,
            password=enc,
        )

        output = cli.run_command(command)
        cli.disconnect()

        console.print(f"\n[bold]{name}:[/bold]")
        for line in output:
            console.print(f"  {line}")

    except Exception as e:
        logging.error(f"Could not run command on {name}: {e}")
        print_error(f"  Error: {e}")
