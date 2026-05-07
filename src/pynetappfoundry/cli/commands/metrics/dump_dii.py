"""Dump metrics from Data Infrastructure Insights.

Rewrites ``nf metrics dump-dii`` to use the DII ``/lake/query/timeseries``
POST endpoint with per-volume granularity, matching the sysadmin reference
script (``dump_cluster_metrics_dii.py``).

Breaking change: ``--days`` is replaced by the required ``--date YYYY-MM-DD``
option. The SQLite database filename now includes the date (e.g.
``<cluster>_2025-04-13_metrics.db``) and each table stores data for one
SVM/volume pair (``{vserver_name}-{volume_name}``).

The aggregation interval and total window length are configurable via
``--interval`` (default ``60s``) and ``--window-days`` (default ``3``,
centered on ``--date``).
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
from pynetappfoundry.db.metrics import _TABLE_NAME_PATTERN, MetricDB
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

_DEFAULT_INTERVAL = "60s"
_DEFAULT_WINDOW_DAYS = 3


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
        "Anchor date in YYYY-MM-DD format. The retrieved window is centered "
        "on this date (see --window-days)."
    ),
)
@click.option(
    "--interval",
    default=_DEFAULT_INTERVAL,
    show_default=True,
    help="Aggregation interval passed to DII (e.g. '60s', '5m', '1h').",
)
@click.option(
    "--window-days",
    "window_days",
    type=int,
    default=_DEFAULT_WINDOW_DAYS,
    show_default=True,
    help=(
        "Total number of UTC days in the query window, centered on --date. "
        "Default 3 yields (date - 1 day) through (date + 2 days)."
    ),
)
@with_config("Dump DII metrics failed")
def dump_dii(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    date: str,
    interval: str,
    window_days: int,
) -> None:
    """Dump per-volume metrics from Data Infrastructure Insights.

    Issues one POST per metric per volume (6 total per volume) to the DII
    ``/lake/query/timeseries`` endpoint and stores the results in a
    per-cluster SQLite database.
    """
    try:
        dii_client = DIIAPIClient(config)
    except Exception as e:
        print_exception(f"Could not initialise DII client: {e}", e)
        return

    try:
        from_ms, to_ms = _compute_window(date, window_days)
    except ValueError as e:
        print_error(f"Invalid window: {e}")
        return

    for name, details in clusters.items():
        _dump_cluster(config, name, details, dii_client, date, from_ms, to_ms, interval)

    print_success("Metrics saved to database")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _compute_window(date_str: str, window_days: int = _DEFAULT_WINDOW_DAYS) -> tuple[int, int]:
    """Compute epoch-millisecond boundaries for a window centered on *date_str*.

    The window length is *window_days* UTC days. The anchor date sits as
    close to the middle of the window as possible; for even *window_days*
    the window leans forward by one day.

    * ``half = (window_days - 1) // 2``
    * ``start = date - half days`` (00:00:00 UTC)
    * ``end   = date + (window_days - half) days`` (00:00:00 UTC)

    For ``window_days=3`` (default) this yields ``date - 1 day`` to
    ``date + 2 days`` — three full UTC days centered on *date*.

    Args:
        date_str: Anchor date in ``YYYY-MM-DD`` format.
        window_days: Total number of UTC days in the window. Must be ≥ 1.

    Returns:
        ``(from_ms, to_ms)`` as integer epoch milliseconds.

    Raises:
        ValueError: If *window_days* is less than 1.

    Example::

        >>> _compute_window("2025-04-13")
        (1744416000000, 1744675200000)
        >>> _compute_window("2025-04-13", window_days=1)
        (1744502400000, 1744588800000)
    """
    if window_days < 1:
        raise ValueError(f"window_days must be ≥ 1, got {window_days}")
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    half = (window_days - 1) // 2
    forward = window_days - half
    from_dt = date - timedelta(days=half)
    to_dt = date + timedelta(days=forward)
    from_ms = int(from_dt.timestamp() * 1000)
    to_ms = int(to_dt.timestamp() * 1000)
    return from_ms, to_ms


def _build_body(
    metric: str,
    svm: str,
    vol: str,
    from_ms: int,
    to_ms: int,
    interval: str = _DEFAULT_INTERVAL,
) -> dict[str, Any]:
    """Build the DII ``/lake/query/timeseries`` POST request body.

    One body is constructed per metric; the caller iterates over
    :data:`_METRICS` and calls this function for each one. The body
    contains only the fields required by the DII OpenAPI schema —
    optional fields (``maxNumberOfDataPoints``, ``detectAnomalies``,
    ``interpolationType``) are omitted to keep the request minimal and
    let the server apply its defaults.

    Args:
        metric: Metric name, e.g. ``"read_ops"``.
        svm: SVM (vserver) name.
        vol: Volume name.
        from_ms: Start of window in epoch milliseconds.
        to_ms: End of window in epoch milliseconds.
        interval: Aggregation interval, e.g. ``"60s"``.

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
        "timeAggregationInterval": interval,
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
    interval: str = _DEFAULT_INTERVAL,
) -> None:
    """Fetch and store metrics for a single volume.

    Issues one ``Query.invoke()`` POST per metric (6 total), merges the
    responses into per-timestamp rows keyed by ``{svm_name}-{vol_name}``,
    validates completeness, and upserts all rows into the ``MetricDB``.

    The ``{svm_name}-{vol_name}`` table name is validated against
    :data:`pynetappfoundry.db.metrics._TABLE_NAME_PATTERN` *before* any
    POSTs are issued; volumes whose names produce an invalid table name
    are skipped with a logged error so the 6 wasted requests are avoided.

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
        interval: Aggregation interval forwarded to :func:`_build_body`.
    """
    table_name = f"{svm_name}-{vol_name}"
    if not _TABLE_NAME_PATTERN.match(table_name):
        print_error(f"Skipping {cluster}:{svm_name}:{vol_name} — invalid table name {table_name!r}")
        logger.warning(
            "Skipping invalid table name %r for %s:%s:%s",
            table_name,
            cluster,
            svm_name,
            vol_name,
        )
        return

    logger.info("  Gathering data for %s:%s:%s", cluster, svm_name, vol_name)
    try:
        current_metrics: dict[int, dict[str, Any]] = {}
        for metric in _METRICS:
            body = _build_body(metric, svm_name, vol_name, from_ms, to_ms, interval)
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

        db.create_table(table_name)
        db.upsert_many(table_name, rows)

    except Exception as e:
        print_error(f"Could not retrieve data for {cluster}:{svm_name}:{vol_name}: {e}")
        logger.exception("Exception for volume %s:%s:%s", cluster, svm_name, vol_name)


def _dump_cluster(
    config: Config,
    name: str,
    details: dict[str, Any],
    dii_client: DIIAPIClient,
    date_str: str,
    from_ms: int,
    to_ms: int,
    interval: str,
) -> None:
    """Dump per-volume metrics for a single cluster.

    Builds an ONTAP client for *name*, lists non-root volumes, opens the
    per-cluster ``MetricDB``, and dispatches each volume to
    :func:`_dump_volume`. Per-cluster exceptions are caught so a failure
    for one cluster does not abort the run.

    Args:
        config: Top-level :class:`Config` instance.
        name: Cluster name (key in the clusters dict).
        details: Cluster details dict (kwargs for :class:`ClusterConfig`).
        dii_client: Shared :class:`DIIAPIClient` for all clusters.
        date_str: Anchor date string used in the DB filename.
        from_ms: Start of window in epoch milliseconds.
        to_ms: End of window in epoch milliseconds.
        interval: Aggregation interval forwarded to :func:`_dump_volume`.
    """
    print_info(f"Getting metrics for {name}...")
    try:
        cluster_config = ClusterConfig(**details)
        ontap_client = ONTAPAPIClient(cluster=cluster_config, config=config)

        volumes: list[OntapVolume] = (
            QuerySet(OntapVolume, ontap_client, config=config).filter(is_svm_root=False).all()
        )

        if not volumes:
            print_warning(f"No volumes found for {name}")
            return

        db = MetricDB(config, db_name=f"{name}_{date_str}_metrics.db")
        dii_query = Query(dii_client, "/lake/query/timeseries")

        for volume in volumes:
            _dump_volume(
                name,
                volume.name,
                volume.svm.name,
                dii_query,
                db,
                from_ms,
                to_ms,
                interval,
            )

        print_debug(f"Metrics saved for {name}")

    except Exception as e:
        print_error(f"Could not dump metrics for {name}: {e}")
        logger.exception("Exception for cluster %s", name)
