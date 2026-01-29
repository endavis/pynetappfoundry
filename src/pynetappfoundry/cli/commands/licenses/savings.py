"""Calculate license savings information."""

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
@with_config("License savings calculation failed")
def savings(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Calculate license savings information.

    Analyzes license usage across clusters to identify potential savings.
    """
    for name, details in clusters.items():
        print_info(f"Analyzing license savings for {name}...")
        _analyze_cluster_savings(name, details, config)


def _analyze_cluster_savings(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> None:
    """Analyze savings for a single cluster."""
    user, password = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=password,
            verify=False,
        ):
            table = Table(title=f"License Usage for {name}")
            table.add_column("Package")
            table.add_column("License Type")
            table.add_column("Used Capacity")
            table.add_column("Entitled Capacity")

            for lic in LicensePackage.get_collection(fields="*"):
                lic_dict = lic.to_dict()
                for item in lic_dict.get("licenses", []):
                    serial = item.get("serial_number", "")
                    license_type = "Standard"

                    if serial.startswith("9092"):
                        license_type = "Cloud Capacity"
                    elif serial.startswith("2265"):
                        license_type = "Data Tiering"
                    elif serial.startswith("3200"):
                        license_type = "ONTAP Select"

                    table.add_row(
                        lic_dict.get("name", "Unknown"),
                        license_type,
                        str(item.get("capacity", {}).get("used_size", "N/A")),
                        str(item.get("capacity", {}).get("maximum_size", "N/A")),
                    )

            console.print(table)

    except Exception as e:
        logging.error(f"Could not analyze savings for {name}: {e}")
        print_error(f"  Error: {e}")
