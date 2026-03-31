"""Get license information from clusters."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import click
from rich.table import Table

import pynetappfoundry.cache.ontap.cluster.licensing.licenses.mapping  # noqa: F401 - register TypeMapping
from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import console, print_error, print_info
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.models.ontap.cluster.licensing.licenses import (
    OntapLicensePackageResponse,
)
from pynetappfoundry.query import QuerySet

# Column headers used for both table and CSV output
COLUMNS = ("Cluster", "License Description", "Node", "Serial #", "Expiration")

# Row type alias
LicenseRow = tuple[str, str, str, str, str]


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--csv",
    "csv_output",
    is_flag=True,
    default=False,
    help="Output to CSV file instead of console table.",
)
@click.option(
    "--output",
    "-o",
    "output_file",
    type=click.Path(),
    default=None,
    help="CSV output file path (default: timestamped file in output dir).",
)
@with_config("Get licenses failed")
def get(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    csv_output: bool,
    output_file: str | None,
) -> None:
    """Get license information from clusters.

    Retrieves and displays license packages from matching clusters.
    Filters out licenses without expiry or with owner 'none'.
    Flags clusters missing a Cloud ONTAP License.
    """
    all_rows: list[LicenseRow] = []

    for name, details in clusters.items():
        print_info(f"Getting licenses for {name}...")
        rows = _get_cluster_licenses(name, details, config)
        all_rows.extend(rows)

    if csv_output:
        _write_csv(all_rows, config, output_file)
    else:
        _print_table(all_rows)


def _get_cluster_licenses(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> list[LicenseRow]:
    """Get licenses from a single cluster.

    Args:
        name: Cluster name.
        details: Cluster connection details.
        config: Application configuration.

    Returns:
        List of license row tuples for this cluster.
    """
    try:
        cluster_config = ClusterConfig(**details)
        client = ONTAPAPIClient(cluster=cluster_config, config=config)

        packages: list[OntapLicensePackageResponse] = QuerySet(
            OntapLicensePackageResponse, client
        ).all()

        rows: list[LicenseRow] = []

        for pkg in packages:
            for lic in pkg.licenses:
                if not lic.owner or lic.owner.lower() == "none":
                    continue

                rows.append(
                    (
                        name,
                        pkg.description,
                        lic.owner,
                        lic.serial_number,
                        lic.expiry_time or "No expiry",
                    )
                )

        return rows

    except Exception as e:
        print_error(f"Could not retrieve licenses for {name}: {e}")
        return []


def _print_table(rows: list[LicenseRow]) -> None:
    """Print license rows as a Rich table.

    Args:
        rows: License row tuples.
    """
    table = Table(title="Cluster Licenses")
    for col in COLUMNS:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def _write_csv(
    rows: list[LicenseRow],
    config: Config,
    output_file: str | None,
) -> None:
    """Write license rows to a CSV file.

    Args:
        rows: License row tuples.
        config: Application configuration (for default output dir).
        output_file: Explicit output path, or None for timestamped default.
    """
    if output_file:
        path = Path(output_file)
    else:
        timestamp = datetime.now(tz=UTC).strftime("%Y-%m-%d_%H-%M-%S")
        path = Path(config.output_dir) / f"get_licenses_{timestamp}.csv"

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(rows)

    print_info(f"CSV written to {path}")
