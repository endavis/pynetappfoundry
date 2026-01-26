"""Generate client lock reports."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import click
from openpyxl import Workbook

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_info, print_success
from pynetappfoundry.core.config import Config


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Locks report failed")
def locks(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Generate client lock reports.

    Creates an Excel workbook with all client locks across
    matching clusters.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config.output_dir / f"locks_{timestamp}.xlsx"
    wb = Workbook()

    # Remove default sheet
    default_sheet = wb.active
    if default_sheet:
        wb.remove(default_sheet)

    for name, details in clusters.items():
        print_info(f"Gathering lock data for {name}...")
        _gather_lock_data(name, details, config, wb)

    wb.save(filename)
    print_success(f"Report saved to {filename}")


def _gather_lock_data(
    name: str,
    details: dict[str, Any],
    config: Config,
    wb: Workbook,
) -> None:
    """Gather lock data from a single cluster."""
    from netapp_ontap import HostConnection
    from netapp_ontap.resources import ClientLock

    user, enc = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=enc,
            verify=False,
        ):
            ws = wb.create_sheet(name)
            ws.append([
                "Volume", "Protocol", "Type", "Path",
                "Lock", "State", "IP Address"
            ])

            locks_data: list[dict[str, Any]] = []
            for lock in ClientLock.get_collection(fields="*"):
                locks_data.append(lock.to_dict())

            logging.info(f"Locks found: {len(locks_data)}")

            for item in locks_data:
                try:
                    lock_type = item.get("type", "unknown")
                    if lock_type == "share_level":
                        ws.append([
                            item.get("volume", {}).get("name", "Unknown"),
                            item.get("protocol", "Unknown"),
                            lock_type,
                            item.get("path", "Unknown"),
                            str(item.get("share_lock", "")),
                            item.get("state", "Unknown"),
                            item.get("client_address", "Unknown"),
                        ])
                    elif lock_type == "op_lock":
                        ws.append([
                            item.get("volume", {}).get("name", "Unknown"),
                            item.get("protocol", "Unknown"),
                            lock_type,
                            item.get("path", "Unknown"),
                            str(item.get("oplock_level", "")),
                            item.get("state", "Unknown"),
                            item.get("client_address", "Unknown"),
                        ])
                    else:
                        logging.info(f"Unknown lock type: {lock_type}")
                except Exception as e:
                    logging.error(f"Lock error: {e}")

    except Exception as e:
        logging.error(f"Could not gather lock data for {name}: {e}")
        ws = wb.create_sheet(name)
        ws.append(["Error", str(e)])
