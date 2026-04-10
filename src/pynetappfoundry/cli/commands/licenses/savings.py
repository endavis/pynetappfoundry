"""Calculate license savings information."""

from __future__ import annotations

from typing import Any

import click
from rich.table import Table

import pynetappfoundry.cache.ontap.cluster.licensing.licenses.mapping  # noqa: F401
from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import console, print_error, print_info
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.models.ontap.cluster.licensing.licenses import OntapLicensePackageResponse
from pynetappfoundry.query import QuerySet


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
    try:
        cluster_config = ClusterConfig(**details)
        client = ONTAPAPIClient(cluster=cluster_config, config=config)

        packages: list[OntapLicensePackageResponse] = QuerySet(
            OntapLicensePackageResponse, client, config=config
        ).all()

        table = Table(title=f"License Usage for {name}")
        table.add_column("Package")
        table.add_column("License Type")
        table.add_column("Used Capacity")
        table.add_column("Entitled Capacity")

        for pkg in packages:
            for lic in pkg.licenses:
                serial = lic.serial_number
                license_type = "Standard"

                if serial.startswith("9092"):
                    license_type = "Cloud Capacity"
                elif serial.startswith("2265"):
                    license_type = "Data Tiering"
                elif serial.startswith("3200"):
                    license_type = "ONTAP Select"

                table.add_row(
                    pkg.name or "Unknown",
                    license_type,
                    str(lic.capacity.used_size or "N/A"),
                    str(lic.capacity.maximum_size or "N/A"),
                )

        console.print(table)

    except Exception as e:
        print_error(f"Could not analyze savings for {name}: {e}")
