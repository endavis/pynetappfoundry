"""Cache refresh orchestration.

Builds the ONTAP clients for each cluster, collects metadata, diffs it against
the previous snapshot, and persists the result to the cache and history
databases.  The CLI (``nf cache refresh``) owns option parsing, the database
lifecycle and rendering; it plugs into this module through the
:class:`RefreshObserver` protocol.

Threading model (ADR-0014): worker threads only run :func:`_collect_cluster`,
which takes **no database handle**.  Every database read and write happens on
the thread that calls :meth:`CacheRefresher.run`, because SQLite connections
cannot cross threads.  ``workers <= 1`` runs the same pipeline inline without
constructing a ``ThreadPoolExecutor``.
"""

from __future__ import annotations

import contextlib
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Protocol

from pynetappfoundry.cache._base import is_schema_compatible
from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.collector import MetadataCollector, ProgressInfo
from pynetappfoundry.cache.diff import compute_diff
from pynetappfoundry.clients.ontap import ONTAPCLI, ONTAPAPIClient
from pynetappfoundry.core.models import ClusterConfig

if TYPE_CHECKING:
    from collections.abc import Sequence
    from concurrent.futures import Future

    from pynetappfoundry.cache.db import ClusterMetadataDB
    from pynetappfoundry.cache.history_db import CacheHistoryDB
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

__all__ = [
    "CacheRefresher",
    "ClusterProgress",
    "ClusterRefreshResult",
    "ProgressInfo",
    "RefreshObserver",
    "RefreshStatus",
    "RefreshSummary",
    "categorize_failure",
    "effective_workers",
]


class RefreshStatus(Enum):
    """Outcome of refreshing one cluster."""

    OK = "ok"
    NO_CLIENTS = "no_clients"
    COLLECT_FAILED = "collect_failed"
    PERSIST_FAILED = "persist_failed"


def categorize_failure(error: Exception) -> tuple[str, str]:
    """Categorize a collection failure for the failure summary.

    Args:
        error: The exception that caused the failure.

    Returns:
        Tuple of (category, detail) for display.
    """
    error_str = str(error)
    error_type = type(error).__name__

    if "CLI_FAILURE" in error_str:
        return "CLI", error_str.split("CLI_FAILURE: ", 1)[
            -1
        ] if "CLI_FAILURE: " in error_str else f"{error_type}: {error}"
    if "API_FAILURE" in error_str or "Collection failed for phase" in error_str:
        return "API", error_str.split("API_FAILURE: ", 1)[
            -1
        ] if "API_FAILURE: " in error_str else f"{error_type}: {error}"
    return "API", f"{error_type}: {error}"


def effective_workers(requested: int, n_clusters: int) -> int:
    """Return the worker count to use for ``n_clusters`` clusters.

    A single cluster always runs inline regardless of the requested count.

    Args:
        requested: Requested number of parallel cluster workers.
        n_clusters: Number of clusters to refresh.

    Returns:
        ``1`` for zero or one cluster, otherwise ``min(requested, n_clusters)``.
    """
    return 1 if n_clusters <= 1 else min(requested, n_clusters)


@dataclass(frozen=True)
class ClusterRefreshResult:
    """Outcome of refreshing a single cluster."""

    cluster_name: str
    status: RefreshStatus
    error: Exception | None = None

    @property
    def failure(self) -> str | None:
        """Failure description for the summary, or ``None`` when successful."""
        if self.status is RefreshStatus.OK:
            return None
        if self.status is RefreshStatus.NO_CLIENTS:
            return "No clients available"
        err = self.error or RuntimeError("Unknown collection failure")
        category, detail = categorize_failure(err)
        return f"{category}: {detail}"


@dataclass(frozen=True)
class RefreshSummary:
    """Results of a whole refresh run."""

    results: list[ClusterRefreshResult] = field(default_factory=list)

    @property
    def succeeded(self) -> int:
        """Number of clusters refreshed successfully."""
        return sum(1 for r in self.results if r.status is RefreshStatus.OK)

    @property
    def failed(self) -> int:
        """Number of clusters that failed."""
        return len(self.results) - self.succeeded

    @property
    def failures(self) -> dict[str, list[str]]:
        """Failure descriptions per cluster name."""
        out: dict[str, list[str]] = {}
        for r in self.results:
            message = r.failure
            if message is not None:
                out.setdefault(r.cluster_name, []).append(message)
        return out


class ClusterProgress(Protocol):
    """Per-cluster progress sink; may be called from a worker thread."""

    def on_phase(self, info: ProgressInfo) -> None:
        """Handle a collector phase update."""

    def on_client_unavailable(self, kind: str, error: Exception) -> None:
        """Report that the ``"API"`` or ``"CLI"`` client could not be built."""

    def on_collection_finished(self, success: bool) -> None:
        """Report that collection ended (clients existed), with its outcome."""


class RefreshObserver(Protocol):
    """Receives refresh events on the thread that calls ``run``."""

    def cluster_started(self, name: str, index: int, total: int) -> ClusterProgress | None:
        """Called before a cluster is collected; returns its progress sink."""

    def cluster_finished(
        self,
        result: ClusterRefreshResult,
        progress: ClusterProgress | None,
        completed: int,
        total: int,
    ) -> None:
        """Called once per cluster after persistence (or failure)."""


@dataclass
class _CollectResult:
    """Result of a cluster collection.

    Carries everything the persisting thread needs (metadata and the previous
    snapshot used for the diff).
    """

    cluster_name: str
    metadata: CachedClusterMetadata | None
    previous_metadata: CachedClusterMetadata | None
    success: bool
    error: Exception | None
    no_clients: bool


def _collect_cluster(
    config: Config,
    cluster_name: str,
    previous_metadata: CachedClusterMetadata | None,
    *,
    progress: ClusterProgress | None,
) -> _CollectResult:
    """Collect metadata for a single cluster (worker-thread safe).

    Takes **zero DB handles**. Builds API/CLI clients and runs the collector,
    using the caller-supplied ``previous_metadata`` (loaded on the persisting
    thread). Never reads or writes the cache or history database.
    """
    cluster_data = config.data["clusters"][cluster_name]
    ip = cluster_data.get("ip", "")
    user, password = config.get_user("clusters", cluster_name)
    cluster_obj = ClusterConfig(name=cluster_name, ip=ip)

    api_client: ONTAPAPIClient | None = None
    cli_client: ONTAPCLI | None = None

    try:
        api_client = ONTAPAPIClient(cluster=cluster_obj, config=config)
        logger.debug("[%s] API client initialized", cluster_name)
    except Exception as e:
        if progress is not None:
            progress.on_client_unavailable("API", e)
        logger.warning("[%s] API client unavailable: %s", cluster_name, e)

    try:
        cli_client = ONTAPCLI(
            name=cluster_name,
            host_or_ip=ip,
            username=user,
            password=password,
            trust_store=config.get_trust_store(),
        )
        logger.debug("[%s] CLI client initialized", cluster_name)
    except Exception as e:
        if progress is not None:
            progress.on_client_unavailable("CLI", e)
        logger.warning("[%s] CLI client unavailable: %s", cluster_name, e)

    if not api_client and not cli_client:
        logger.error("[%s] No clients available", cluster_name)
        return _CollectResult(
            cluster_name=cluster_name,
            metadata=None,
            previous_metadata=None,
            success=False,
            error=None,
            no_clients=True,
        )

    aws_sso_config = config.settings.get("aws", {}).get("sso")

    collector = MetadataCollector(
        api_client=api_client,
        cli_client=cli_client,
        progress_callback=progress.on_phase if progress is not None else None,
        aws_sso_config=aws_sso_config,
    )

    error: Exception | None = None
    metadata: CachedClusterMetadata | None = None
    try:
        metadata = collector.collect_all(cluster_name)
    except Exception as e:
        error = e
        logger.warning("[%s] Collection failed: %s", cluster_name, e)

    success = error is None and metadata is not None
    try:
        if progress is not None:
            progress.on_collection_finished(success)
    finally:
        # Disconnect regardless of outcome; not DB-related, safe in a worker.
        if cli_client:
            with contextlib.suppress(Exception):
                cli_client.disconnect()
                logger.debug("[%s] CLI client disconnected", cluster_name)

    return _CollectResult(
        cluster_name=cluster_name,
        metadata=metadata,
        previous_metadata=previous_metadata,
        success=success,
        error=error,
        no_clients=False,
    )


class CacheRefresher:
    """Refreshes cluster metadata into the cache and history databases.

    The caller owns the database handles (and closes them); this class only
    reads and writes through them, always on the thread calling :meth:`run`.
    """

    def __init__(
        self,
        config: Config,
        db: ClusterMetadataDB,
        history_db: CacheHistoryDB,
    ) -> None:
        """Initialize the refresher.

        Args:
            config: Configuration object.
            db: Cache database (not closed by this class).
            history_db: History database (not closed by this class).
        """
        self._config = config
        self._db = db
        self._history_db = history_db

    def run(
        self,
        clusters: Sequence[str],
        *,
        workers: int,
        observer: RefreshObserver,
    ) -> RefreshSummary:
        """Refresh ``clusters`` and return the per-cluster results.

        Args:
            clusters: Cluster names to refresh.
            workers: Parallel cluster workers; ``<= 1`` runs inline.
            observer: Receives start/finish events on the calling thread.

        Returns:
            A :class:`RefreshSummary` with one result per cluster.
        """
        total = len(clusters)
        results: list[ClusterRefreshResult] = []

        if workers <= 1:
            for idx, name in enumerate(clusters, 1):
                logger.info("Processing cluster: %s (%d/%d)", name, idx, total)
                progress = observer.cluster_started(name, idx, total)
                previous = self._load_previous(name)
                collected: _CollectResult | None = None
                error: Exception | None = None
                try:
                    collected = _collect_cluster(self._config, name, previous, progress=progress)
                except Exception as e:
                    error = e
                results.append(self._finish(name, collected, error, progress, idx, total, observer))
            return RefreshSummary(results)

        # Preload previous snapshots on the calling thread: SQLite connections
        # can't cross threads, so workers must not touch history_db.
        previous_by_cluster = {name: self._load_previous(name) for name in clusters}
        completed = 0
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_map: dict[Future[_CollectResult], tuple[str, ClusterProgress | None]] = {}
            for idx, name in enumerate(clusters, 1):
                progress = observer.cluster_started(name, idx, total)
                logger.info("Queued cluster for refresh: %s (of %d)", name, total)
                future = executor.submit(
                    _collect_cluster,
                    self._config,
                    name,
                    previous_by_cluster[name],
                    progress=progress,
                )
                future_map[future] = (name, progress)

            for future in as_completed(future_map):
                completed += 1
                name, progress = future_map[future]
                par_collected: _CollectResult | None = None
                par_error: Exception | None = None
                try:
                    par_collected = future.result()
                except Exception as e:
                    par_error = e
                results.append(
                    self._finish(
                        name, par_collected, par_error, progress, completed, total, observer
                    )
                )
        return RefreshSummary(results)

    def _load_previous(self, cluster_name: str) -> CachedClusterMetadata | None:
        """Load the previous cluster snapshot from history, if any."""
        latest_snapshot = self._history_db.get_latest_snapshot(cluster_name)
        if not latest_snapshot:
            return None

        after_json = latest_snapshot.get("after_json")
        if not (after_json and isinstance(after_json, str)):
            return None

        try:
            previous_data = json.loads(after_json)
            snapshot_version = previous_data.get("cache_version")

            if not is_schema_compatible(snapshot_version):
                logger.warning(
                    "Previous snapshot for %s has incompatible schema version %s, "
                    "treating as initial capture",
                    cluster_name,
                    snapshot_version,
                )
                return None

            previous_metadata = CachedClusterMetadata.model_validate(previous_data)
            logger.debug("Found previous snapshot for %s (v%s)", cluster_name, snapshot_version)
            return previous_metadata
        except Exception as e:
            logger.warning("Failed to parse previous snapshot for %s: %s", cluster_name, e)
            return None

    def _finish(
        self,
        name: str,
        collected: _CollectResult | None,
        error: Exception | None,
        progress: ClusterProgress | None,
        completed: int,
        total: int,
        observer: RefreshObserver,
    ) -> ClusterRefreshResult:
        """Classify a collection, persist it, and notify the observer."""
        result: ClusterRefreshResult
        if collected is None:
            logger.error("Failed to process cluster %s: %s", name, error)
            result = ClusterRefreshResult(name, RefreshStatus.COLLECT_FAILED, error)
        elif collected.no_clients:
            logger.error("No clients available for %s", name)
            result = ClusterRefreshResult(name, RefreshStatus.NO_CLIENTS)
        elif collected.error is not None or collected.metadata is None:
            err = collected.error or RuntimeError("Unknown collection failure")
            logger.error("Failed to process cluster %s: %s", name, err)
            result = ClusterRefreshResult(name, RefreshStatus.COLLECT_FAILED, err)
        else:
            try:
                self._persist(collected)
                result = ClusterRefreshResult(name, RefreshStatus.OK)
            except Exception as e:
                logger.exception("Persist failed for cluster %s", name)
                result = ClusterRefreshResult(name, RefreshStatus.PERSIST_FAILED, e)
        observer.cluster_finished(result, progress, completed, total)
        return result

    def _persist(self, result: _CollectResult) -> None:
        """Diff, record history and write the cache for one collected cluster."""
        assert result.metadata is not None, "must have metadata to persist"
        cluster_name = result.cluster_name
        metadata = result.metadata
        previous_metadata = result.previous_metadata

        # Defence-in-depth: SQLite writes must stay on the calling thread.
        if threading.current_thread() is not threading.main_thread():
            logger.warning(
                "[%s] persisting off the main thread (%s); SQLite writes may race.",
                cluster_name,
                threading.current_thread().name,
            )

        changes = compute_diff(previous_metadata, metadata)

        if previous_metadata is None or changes:
            before_json = previous_metadata.model_dump_json() if previous_metadata else None
            after_json = metadata.model_dump_json()
            change_id = self._history_db.record_change(
                cluster_name=cluster_name,
                before_json=before_json,
                after_json=after_json,
                summary=changes,
            )
            if previous_metadata is None:
                logger.info(
                    "[%s] Initial snapshot recorded (change_id=%d)", cluster_name, change_id
                )
            else:
                logger.info(
                    "[%s] Change recorded: %d changes (change_id=%d)",
                    cluster_name,
                    len(changes),
                    change_id,
                )
        else:
            logger.info("[%s] No changes detected, history not updated", cluster_name)

        self._db.set(cluster_name, metadata)
        logger.info("[%s] Cache updated", cluster_name)
