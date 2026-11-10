"""Run CLI commands on clusters."""

from __future__ import annotations

from typing import Any

import click
from rich.markup import escape

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import console, print_exception, print_info
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
    failed: list[str] = []
    for name, details in clusters.items():
        print_info(f"Running command on {name}...")
        if not _run_cluster_command(name, details, config, command):
            failed.append(name)

    if failed:
        raise click.ClickException(
            f"Command failed on {len(failed)} cluster(s): {', '.join(failed)}"
        )


def _run_cluster_command(
    name: str,
    details: dict[str, Any],
    config: Config,
    command: str,
) -> bool:
    """Run command on a single cluster.

    Returns:
        True on success, False if the command failed.
    """
    user, password = config.get_user("clusters", name)

    try:
        cli = ONTAPCLI(
            name=name,
            host_or_ip=details["ip"],
            username=user,
            password=password,
        )

        output = cli.run_command(command)
        cli.disconnect()

        console.print(f"\n[bold]{escape(name)}:[/bold]")
        for line in output:
            console.print(f"  {escape(line)}")
        return True

    except Exception as e:
        print_exception(f"Could not run command on {name}: {e}", e)
        return False
