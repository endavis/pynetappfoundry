"""Dump metrics from Data Infrastructure Insights.

Rewrites ``nf metrics dump-dii`` to use the DII ``/lake/query/timeseries``
POST endpoint with per-volume granularity, matching the sysadmin reference
script (``dump_cluster_metrics_dii.py``).

Breaking change: ``--days`` is replaced by the required ``--date YYYY-MM-DD``
option. The SQLite database filename now includes the date (e.g.
``<cluster>_2025-04-13_metrics.db``) and each table stores data for one
SVM/volume pair (``{vserver_name}-{volume_name}``).
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import (
    print_debug,
    print_error,
    print_exception,
    print_info,
    print_success,
    print_warning,
)
from pynetappfoundry.clients.dii.api import DIIAPIClient
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.db.metrics import MetricDB
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.query import Query, QuerySet

logger = logging.getLogger(__name__)

#: Ordered list of DII workload_volume metrics fetched for every volume.
_METRICS: list[str] = [
    "read_ops",
    "write_ops",
    "read_throughput",
    "write_throughput",
    "read_latency",
    "write_latency",
]


@click.command("dump-dii")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--date",
    "-d",
    "date",
    required=True,
    help=(
        "Date in YYYY-MM-DD format.  Retrieves a 3-day window: "
        "(date - 1 day) 00:00:00 UTC → (date + 2 days) 00:00:00 UTC."
    ),
)
@with_config("Dump DII metrics failed")
def dump_dii(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    date: str,
) -> None:
    """Dump per-volume metrics from Data Infrastructure Insights.

    Issues one POST per metric per volume to the DII
    ``/lake/query/timeseries`` endpoint with a 60-second aggregation
    interval and stores the results in a per-cluster SQLite database.
    """
    try:
        dii_client = DIIAPIClient(config)
    except Exception as e:
        print_exception(f"Could not initialise DII client: {e}", e)
        return

    from_ms, to_ms = _compute_window(date)

    for name, details in clusters.items():
        print_info(f"Getting metrics for {name}...")
        try:
            cluster_config = ClusterConfig(**details)
            ontap_client = ONTAPAPIClient(cluster=cluster_config, config=config)

            volumes: list[OntapVolume] = (
                QuerySet(OntapVolume, ontap_client, config=config).filter(is_svm_root=False).all()
            )

            if not volumes:
                print_warning(f"No volumes found for {name}")
                continue

            db = MetricDB(config, db_name=f"{name}_{date}_metrics.db")
            dii_query = Query(dii_client, "/lake/query/timeseries")

            for volume in volumes:
                vol_name = volume.name
                svm_name = volume.svm.name
                _dump_volume(name, vol_name, svm_name, dii_query, db, from_ms, to_ms)

            print_debug(f"Metrics saved for {name}")

        except Exception as e:
            print_error(f"Could not dump metrics for {name}: {e}")
            logger.exception("Exception for cluster %s", name)

    print_success("Metrics saved to database")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _compute_window(date_str: str) -> tuple[int, int]:
    """Compute epoch-millisecond boundaries for a 3-day window around *date_str*.

    The window starts at ``(date - 1 day) 00:00:00 UTC`` and ends at
    ``(date + 2 days) 00:00:00 UTC``.

    Args:
        date_str: Date in ``YYYY-MM-DD`` format.

    Returns:
        ``(from_ms, to_ms)`` as integer epoch milliseconds.

    Example::

        >>> _compute_window("2025-04-13")
        (1744416000000, 1744675200000)
    """
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    from_dt = date - timedelta(days=1)
    to_dt = date + timedelta(days=2)
    from_ms = int(from_dt.timestamp() * 1000)
    to_ms = int(to_dt.timestamp() * 1000)
    return from_ms, to_ms


def _build_body(
    metric: str,
    svm: str,
    vol: str,
    from_ms: int,
    to_ms: int,
) -> dict[str, Any]:
    """Build the DII ``/lake/query/timeseries`` POST request body.

    One body is constructed per metric; the caller iterates over
    :data:`_METRICS` and calls this function for each one.

    Args:
        metric: Metric name, e.g. ``"read_ops"``.
        svm: SVM (vserver) name.
        vol: Volume name.
        from_ms: Start of window in epoch milliseconds.
        to_ms: End of window in epoch milliseconds.

    Returns:
        Request body dict suitable for ``Query.invoke(body=...)``.
    """
    return {
        "category": "netapp_ontap",
        "measurement": "workload_volume",
        "metric": metric,
        "filter": f'vserver_name = "{svm}" AND volume_name = "{vol}"',
        "fromTimeMs": from_ms,
        "toTimeMs": to_ms,
        "timeAggregationInterval": "60s",
        "maxNumberOfDataPoints": (to_ms - from_ms) // 60_000,
        "detectAnomalies": False,
        "interpolationType": "NONE",
    }


def _parse_timeseries(
    response: Any,
    metric_name: str,
) -> dict[int, dict[str, Any]]:
    """Parse a single-metric DII timeseries response into a timestamp-keyed dict.

    Each data point becomes ``{timestamp_seconds: {metric_name: value}}``.

    Args:
        response: Raw value returned by ``Query.invoke()``; expected to be a
            list whose first element contains a ``"timeseries"`` key.
        metric_name: Name of the metric (used as the inner dict key).

    Returns:
        Mapping from integer timestamp (seconds) to
        ``{metric_name: value}``.  Returns an empty dict when *response* is
        falsy or has an unexpected shape.
    """
    result: dict[int, dict[str, Any]] = {}
    if not response:
        return result
    try:
        timeseries = response[0]["timeseries"]
    except (IndexError, KeyError, TypeError):
        logger.debug("Unexpected response shape for metric %s: %r", metric_name, response)
        return result
    for data in timeseries:
        try:
            ts = int(data["time"]) // 1000
            value = data["value"]
            result[ts] = {metric_name: value}
        except (KeyError, TypeError, ValueError) as exc:
            logger.debug("Skipping bad data point for %s: %r (%s)", metric_name, data, exc)
    return result


def _validate_and_clean(
    metrics_data: dict[int, dict[str, Any]],
    metric_names: list[str],
) -> list[dict[str, Any]]:
    """Validate merged per-timestamp data and drop incomplete placeholder rows.

    * Drops timestamps whose dict contains **only** the ``"timestamp"`` key
      (placeholder rows where all metric POSTs returned no data).
    * Logs an error for timestamps that have some — but not all — expected
      metrics, then still includes them in the output so partial data is
      not silently lost.

    Args:
        metrics_data: Mapping of timestamp (seconds) → row dict that
            includes the ``"timestamp"`` key plus zero or more metric keys.
        metric_names: Ordered list of expected metric column names
            (excluding ``"timestamp"``).

    Returns:
        List of row dicts ready for ``MetricDB.upsert_many()``.
    """
    expected_keys = len(metric_names) + 1  # +1 for "timestamp"
    rows: list[dict[str, Any]] = []
    for ts, row in metrics_data.items():
        row_len = len(row)
        if row_len == 1 and "timestamp" in row:
            # Placeholder with no metric data — drop silently.
            logger.debug("Dropping placeholder-only timestamp %d", ts)
            continue
        if row_len != expected_keys:
            logger.error(
                "Timestamp %d does not have %d keys (has %d): %r",
                ts,
                expected_keys,
                row_len,
                row,
            )
        rows.append(row)
    return rows


def _dump_volume(
    cluster: str,
    vol_name: str,
    svm_name: str,
    dii_query: Query,
    db: MetricDB,
    from_ms: int,
    to_ms: int,
) -> None:
    """Fetch and store metrics for a single volume.

    Issues one ``Query.invoke()`` POST per metric (6 total), merges the
    responses into per-timestamp rows keyed by ``{svm_name}-{vol_name}``,
    validates completeness, and upserts all rows into the ``MetricDB``.

    Per-volume exceptions are caught and logged so that a failure for one
    volume does not prevent sibling volumes from being processed.

    Args:
        cluster: Cluster name (used in log messages only).
        vol_name: Volume name.
        svm_name: SVM (vserver) name.
        dii_query: Bound :class:`~pynetappfoundry.query.Query` instance
            for the ``/lake/query/timeseries`` endpoint.
        db: :class:`~pynetappfoundry.db.metrics.MetricDB` instance for
            this cluster+date.
        from_ms: Start of window in epoch milliseconds.
        to_ms: End of window in epoch milliseconds.
    """
    logger.info("  Gathering data for %s:%s:%s", cluster, svm_name, vol_name)
    try:
        current_metrics: dict[int, dict[str, Any]] = {}
        for metric in _METRICS:
            body = _build_body(metric, svm_name, vol_name, from_ms, to_ms)
            response = dii_query.invoke(body=body)
            parsed = _parse_timeseries(response, metric)
            for ts, metric_dict in parsed.items():
                if ts not in current_metrics:
                    current_metrics[ts] = {"timestamp": ts}
                current_metrics[ts].update(metric_dict)

        rows = _validate_and_clean(current_metrics, _METRICS)
        if not rows:
            logger.info("No data for %s:%s:%s", cluster, svm_name, vol_name)
            return

        table_name = f"{svm_name}-{vol_name}"
        db.create_table(table_name)
        db.upsert_many(table_name, rows)

    except Exception as e:
        print_error(f"Could not retrieve data for {cluster}:{svm_name}:{vol_name}: {e}")
        logger.exception("Exception for volume %s:%s:%s", cluster, svm_name, vol_name)
