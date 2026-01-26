"""Save Azure maintenance events."""

from __future__ import annotations

import logging
from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_info, print_success
from pynetappfoundry.core.config import Config
from pynetappfoundry.db.azevents import AzEventsDB


@click.command("save-azure")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Save Azure events failed")
def save_azure(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Save Azure maintenance events to database.

    Retrieves Azure scheduled events and stores them in SQLite.
    """
    db = AzEventsDB(config)

    for name, details in clusters.items():
        # Skip non-Azure clusters
        if details.get("cloud", "").lower() != "azure":
            continue

        print_info(f"Getting Azure events for {name}...")
        _save_cluster_azure_events(name, details, config, db)

    print_success("Azure events saved to database")


def _save_cluster_azure_events(
    name: str,
    details: dict[str, Any],
    config: Config,
    db: AzEventsDB,
) -> None:
    """Save Azure events from a single cluster."""
    from netapp_ontap import HostConnection
    from netapp_ontap.resources import Node

    user, enc = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=enc,
            verify=False,
        ):
            for node in Node.get_collection(fields="*"):
                node_dict = node.to_dict()
                node_name = node_dict.get("name", "Unknown")

                # Check for Azure scheduled events
                azure_info = node_dict.get("azure", {})
                scheduled_events = azure_info.get("scheduled_events", [])

                for event in scheduled_events:
                    event_id = event.get("event_id", "")
                    if event_id:
                        db_event = {
                            "event_id": event_id,
                            "cluster": name,
                            "node": node_name,
                            "type": event.get("event_type", "Unknown"),
                            "az_maint_not_before": event.get("not_before"),
                            "az_maint_scheduled": event.get("scheduled_time"),
                        }
                        db.upsert_event(db_event)
                        logging.info(f"Saved event {event_id} for {node_name}")

    except Exception as e:
        logging.error(f"Could not get Azure events for {name}: {e}")
