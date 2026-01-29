"""Get events from clusters."""

from __future__ import annotations

from typing import Any

import click
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsEvent
from rich.table import Table

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import console, print_error, print_info
from pynetappfoundry.core.config import Config


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--severity",
    "-s",
    type=click.Choice(["emergency", "alert", "error", "notice", "informational", "debug"]),
    default=None,
    help="Filter by severity level.",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=50,
    help="Maximum number of events to retrieve (default: 50).",
)
@with_config("Get events failed")
def get(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    severity: str | None,
    limit: int,
) -> None:
    """Get events from clusters.

    Retrieves EMS events from matching clusters with optional filtering.
    """
    for name, details in clusters.items():
        print_info(f"Getting events for {name}...")
        _get_cluster_events(name, details, config, severity, limit)


def _get_cluster_events(
    name: str,
    details: dict[str, Any],
    config: Config,
    severity: str | None,
    limit: int,
) -> None:
    """Get events from a single cluster."""
    user, password = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=password,
            verify=False,
        ):
            table = Table(title=f"Events for {name}")
            table.add_column("Time")
            table.add_column("Severity")
            table.add_column("Name")
            table.add_column("Message", max_width=60)

            query_params: dict[str, Any] = {"max_records": limit}
            if severity:
                query_params["severity"] = severity

            count = 0
            for event in EmsEvent.get_collection(**query_params):
                event_dict = event.to_dict()
                table.add_row(
                    str(event_dict.get("time", "Unknown")),
                    event_dict.get("severity", "Unknown"),
                    event_dict.get("message", {}).get("name", "Unknown"),
                    event_dict.get("message", {}).get("text", "")[:60],
                )
                count += 1

            console.print(table)
            print_info(f"Retrieved {count} events")

    except Exception as e:
        print_error(f"Could not retrieve events for {name}: {e}")
