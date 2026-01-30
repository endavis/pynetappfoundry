"""Get events from clusters."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import click
from netapp_ontap.host_connection import HostConnection
from netapp_ontap.resources import EmsEvent
from rich.table import Table

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import console, print_error, print_info, print_success
from pynetappfoundry.core.config import Config


def clean_message(log_message: str, event_name: str) -> str:
    """Clean log message for CSV output.

    Removes event name prefix, replaces commas with semicolons,
    and removes newlines for CSV compatibility.

    Args:
        log_message: The raw log message text.
        event_name: The event name to strip from the message.

    Returns:
        Cleaned message suitable for CSV output.
    """
    return log_message.replace(f"{event_name}: ", "").replace(",", ";").replace("\n", " ").strip()


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
    "--name",
    "-n",
    "event_names",
    multiple=True,
    help="Filter by event name (can specify multiple). Example: -n vsa.mlx.nic.detach",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output to CSV file instead of console.",
)
@click.option(
    "--sort",
    type=click.Choice(["time", "-time"]),
    default="time",
    help="Sort order (default: time ascending, -time for descending).",
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
    event_names: tuple[str, ...],
    output: str | None,
    sort: str,
    limit: int,
) -> None:
    """Get events from clusters.

    Retrieves EMS events from matching clusters with optional filtering.

    Examples:
        nf events get -s error
        nf events get -n vsa.mlx.nic.detach -n vsa.mlx.nic.attach
        nf events get -o events.csv --sort -time
    """
    # Collect all events if outputting to file
    all_events: list[dict[str, Any]] = []
    output_path = Path(output) if output else None

    for name, details in clusters.items():
        print_info(f"Getting events for {name}...")
        events = _get_cluster_events(
            name,
            details,
            config,
            severity,
            event_names,
            sort,
            limit,
            output_to_file=output_path is not None,
        )
        if events:
            all_events.extend(events)

    # Write CSV if output specified
    if output_path and all_events:
        _write_csv(output_path, all_events)
        print_success(f"Events written to {output_path}")
        print_info(f"Total events: {len(all_events)}")


def _get_cluster_events(
    name: str,
    details: dict[str, Any],
    config: Config,
    severity: str | None,
    event_names: tuple[str, ...],
    sort: str,
    limit: int,
    output_to_file: bool = False,
) -> list[dict[str, Any]]:
    """Get events from a single cluster.

    Args:
        name: Cluster name.
        details: Cluster connection details.
        config: Configuration object.
        severity: Optional severity filter.
        event_names: Optional tuple of event names to filter.
        sort: Sort order ("time" or "-time").
        limit: Maximum events to retrieve.
        output_to_file: If True, return events list instead of printing.

    Returns:
        List of event dictionaries if output_to_file, empty list otherwise.
    """
    user, password = config.get_user("clusters", name)
    events: list[dict[str, Any]] = []

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=password,
            verify=False,
        ):
            query_params: dict[str, Any] = {"max_records": limit}

            if severity:
                query_params["severity"] = severity

            if event_names:
                query_params["message.name"] = ",".join(event_names)

            # Handle sort order
            if sort == "-time":
                query_params["order_by"] = "time desc"
            else:
                query_params["order_by"] = "time asc"

            if not output_to_file:
                # Console output with Rich table
                table = Table(title=f"Events for {name}")
                table.add_column("Time")
                table.add_column("Severity")
                table.add_column("Name")
                table.add_column("Message", max_width=60)

            count = 0
            for event in EmsEvent.get_collection(**query_params):
                event_dict = event.to_dict()
                event_time = str(event_dict.get("time", "Unknown"))
                event_severity = event_dict.get("severity", "Unknown")
                message_info = event_dict.get("message", {})
                event_name = message_info.get("name", "Unknown")
                message_text = message_info.get("text", "")

                if output_to_file:
                    # Collect for CSV output
                    events.append(
                        {
                            "cluster": name,
                            "time": event_time,
                            "severity": event_severity,
                            "name": event_name,
                            "message": clean_message(message_text, event_name),
                        }
                    )
                else:
                    # Add to Rich table
                    table.add_row(
                        event_time,
                        event_severity,
                        event_name,
                        message_text[:60],
                    )
                count += 1

            if not output_to_file:
                console.print(table)
                print_info(f"Retrieved {count} events")

    except Exception as e:
        print_error(f"Could not retrieve events for {name}: {e}")

    return events


def _write_csv(output_path: Path, events: list[dict[str, Any]]) -> None:
    """Write events to CSV file.

    Args:
        output_path: Path to output CSV file.
        events: List of event dictionaries to write.
    """
    fieldnames = ["cluster", "time", "severity", "name", "message"]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)
