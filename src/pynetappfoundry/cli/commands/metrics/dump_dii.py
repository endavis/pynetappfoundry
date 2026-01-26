"""Dump metrics from Data Infrastructure Insights."""

from __future__ import annotations

import logging
from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_info, print_success, print_error
from pynetappfoundry.core.config import Config
from pynetappfoundry.clients.dii.api import DIIAPIClient
from pynetappfoundry.db.metrics import MetricDB


@click.command("dump-dii")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--days",
    "-d",
    type=int,
    default=7,
    help="Number of days of history to retrieve (default: 7).",
)
@with_config("Dump DII metrics failed")
def dump_dii(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    days: int,
) -> None:
    """Dump metrics from Data Infrastructure Insights.

    Retrieves performance metrics from DII and stores them in SQLite.
    """
    try:
        dii_client = DIIAPIClient(config)
    except Exception as e:
        print_error(f"Could not initialize DII client: {e}")
        return

    db = MetricDB(config)

    for name, details in clusters.items():
        print_info(f"Getting metrics for {name}...")
        _dump_cluster_metrics(name, details, config, dii_client, db, days)

    print_success("Metrics saved to database")


def _dump_cluster_metrics(
    name: str,
    details: dict[str, Any],
    config: Config,
    dii_client: DIIAPIClient,
    db: MetricDB,
    days: int,
) -> None:
    """Dump metrics for a single cluster."""
    try:
        # Create table for this cluster
        table_name = name.replace("-", "_").replace(".", "_")
        db.create_table(table_name)

        # Get storage assets from DII
        storage_query = {
            "name": name,
        }

        assets = dii_client.call_endpoint(
            "/assets/storages",
            query_params=storage_query,
        )

        if not assets:
            logging.warning(f"No assets found for {name} in DII")
            return

        # Get metrics for each asset
        for asset in assets.get("results", []):
            asset_id = asset.get("id")
            if not asset_id:
                continue

            # Get performance metrics
            metrics_data = dii_client.call_endpoint(
                f"/assets/storages/{asset_id}/performance",
                query_params={"days": days},
            )

            if not metrics_data:
                continue

            # Process and save metrics
            for datapoint in metrics_data.get("datapoints", []):
                metric_record = {
                    "timestamp": datapoint.get("timestamp"),
                    "read_ops": datapoint.get("readOps", 0),
                    "write_ops": datapoint.get("writeOps", 0),
                    "read_latency": datapoint.get("readLatency", 0),
                    "write_latency": datapoint.get("writeLatency", 0),
                    "read_throughput": datapoint.get("readThroughput", 0),
                    "write_throughput": datapoint.get("writeThroughput", 0),
                }
                db.upsert_data(table_name, metric_record)

        logging.info(f"Saved metrics for {name}")

    except Exception as e:
        logging.error(f"Could not dump metrics for {name}: {e}")
