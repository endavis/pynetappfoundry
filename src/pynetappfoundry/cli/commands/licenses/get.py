"""Get license information from clusters."""

from __future__ import annotations

import logging
from typing import Any

import click
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage
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
@with_config("Get licenses failed")
def get(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Get license information from clusters.

    Retrieves and displays all license packages from matching clusters.
    """
    for name, details in clusters.items():
        print_info(f"Getting licenses for {name}...")
        _get_cluster_licenses(name, details, config)


def _get_cluster_licenses(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> None:
    """Get licenses from a single cluster."""
    user, password = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=password,
            verify=False,
        ):
            table = Table(title=f"Licenses for {name}")
            table.add_column("Package")
            table.add_column("Owner")
            table.add_column("Serial Number")
            table.add_column("Expiry")

            for lic in LicensePackage.get_collection(fields="*"):
                lic_dict = lic.to_dict()
                for item in lic_dict.get("licenses", []):
                    table.add_row(
                        lic_dict.get("name", "Unknown"),
                        item.get("owner", "Unknown"),
                        item.get("serial_number", "Unknown"),
                        item.get("expiry_time", "No expiry"),
                    )

            console.print(table)

    except Exception as e:
        logging.error(f"Could not retrieve licenses for {name}: {e}")
        print_error(f"  Error: {e}")
