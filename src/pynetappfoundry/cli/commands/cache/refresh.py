"""Cache refresh command.

Option parsing, database lifecycle and rendering live here. The refresh
orchestration (clients, collection, diffing, persistence) lives in
:mod:`pynetappfoundry.cache.refresher`; this module plugs into it through the
``RefreshObserver`` protocol.
"""

from __future__ import annotations

import io
import json
import logging
import time
from pathlib import Path
from types import TracebackType

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TaskID, TextColumn

from pynetappfoundry.cache import (
    CacheHistoryDB,
    ClusterMetadataDB,
    CollectionPhase,
    ProgressInfo,
)
from pynetappfoundry.cache.refresher import (
    CacheRefresher,
    ClusterProgress,
    ClusterRefreshResult,
    RefreshStatus,
    RefreshSummary,
    effective_workers,
)
from pynetappfoundry.cli.utils import (
    print_error,
    print_exception,
    print_success,
    print_warning,
)
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.logging import setup_logger

console = Console()

# Module logger
logger = logging.getLogger(__name__)


class VerboseProgressDisplay:
    """Displays detailed progress information in verbose mode."""

    def __init__(
        self,
        console: Console,
        cluster_name: str,
        cluster_index: int,
        total_clusters: int,
        buffered: bool = False,
    ) -> None:
        """Initialize the verbose progress display.

        Args:
            console: Rich console for output.
            cluster_name: Name of the cluster being processed.
            cluster_index: 1-based index of the current cluster.
            total_clusters: Total number of clusters to process.
            buffered: When True, skip ``end="\\r"`` starting messages that
                cause cursor-jump garbling when replayed from a capture buffer.
        """
        self.console = console
        self.cluster_name = cluster_name
        self.cluster_index = cluster_index
        self.total_clusters = total_clusters
        self.buffered = buffered
        self.phase_times: dict[CollectionPhase, float] = {}
        self.start_time = time.monotonic()
        self.current_phase: CollectionPhase | None = None

    def on_progress(self, info: ProgressInfo) -> None:
        """Handle progress callback from the collector.

        Args:
            info: Progress information for the current phase.
        """
        if info.status == "starting":
            self.current_phase = info.phase
            # In buffered mode these \r-terminated lines are replayed on a real
            # terminal later, causing cursor-jump garbling — skip them entirely.
            if not self.buffered:
                self.console.print(f"  [dim]|-[/dim] {info.phase_name}...", end="\r")
        elif info.status == "completed":
            self.phase_times[info.phase] = info.elapsed_seconds
            source_str = f" [dim]({info.source})[/dim]" if info.source else ""
            line = f"  [green]|-[/green] {info.phase_name:<20} "
            line += f"{info.elapsed_seconds:>5.1f}s{source_str}"
            self.console.print(line)
        elif info.status == "failed":
            self.phase_times[info.phase] = info.elapsed_seconds
            error_str = f" - {info.error}" if info.error else ""
            line = f"  [red]|-[/red] {info.phase_name:<20} "
            line += f"{info.elapsed_seconds:>5.1f}s [red]FAILED{error_str}[/red]"
            self.console.print(line)

    def print_header(self) -> None:
        """Print the cluster header."""
        self.console.print(
            f"\n[bold][{self.cluster_index}/{self.total_clusters}] {self.cluster_name}[/bold]"
        )

    def print_summary(self, success: bool) -> None:
        """Print the cluster summary.

        Args:
            success: Whether the collection was successful.
        """
        total_time = time.monotonic() - self.start_time
        status = "[green]OK[/green]" if success else "[red]FAILED[/red]"
        self.console.print(f"  [dim]`-[/dim] Total: {total_time:.1f}s {status}")


@click.command()
@click.argument("cluster", required=False)
@click.option(
    "--all",
    "-a",
    "refresh_all",
    is_flag=True,
    help="Refresh cache for all configured clusters.",
)
@click.option(
    "--filter",
    "-f",
    "filter_str",
    help='JSON filter for --all: \'{"env": "Prod", "bu": "Finance"}\'',
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed progress for each collection phase.",
)
@click.option(
    "--parallel-clusters",
    "parallel_clusters",
    type=click.IntRange(min=1),
    default=4,
    show_default=True,
    help=(
        "Number of clusters to process in parallel (with --all). "
        "Use 1 to disable parallelism and preserve strictly sequential behaviour."
    ),
)
@click.pass_context
def refresh(
    ctx: click.Context,
    cluster: str | None,
    refresh_all: bool,
    filter_str: str | None,
    verbose: bool,
    parallel_clusters: int,
) -> None:
    """Refresh the metadata cache for cluster(s).

    If CLUSTER is specified, refresh only that cluster.
    Use --all to refresh all configured clusters.
    Use --filter with --all to refresh only matching clusters.

    Examples:

        nf cache refresh cluster1      # Refresh single cluster
        nf cache refresh --all         # Refresh all clusters
        nf cache refresh --all -v      # Refresh all with detailed progress
        nf cache refresh --all -f '{"env": "Prod"}'  # Refresh only Prod clusters
        nf cache refresh --all --parallel-clusters 8  # More concurrency
    """
    # Always set up file logging
    _, log_file = setup_logger("cache-refresh")
    logger.info("Starting cache refresh operation")

    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        logger.error("Configuration directory not found: %s", config_path)
        ctx.exit(1)

    try:
        config = Config(
            config_dir=config_dir,
            output_dir=ctx.obj.get("output_dir", ""),
            script_name="cache-refresh",
        )
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        logger.exception("Failed to load configuration")
        ctx.exit(1)

    # Parse filter if provided
    filter_dict: dict[str, str] = {}
    if filter_str:
        if not refresh_all:
            print_error("--filter can only be used with --all")
            ctx.exit(1)
        try:
            filter_dict = json.loads(filter_str)
        except json.JSONDecodeError as e:
            print_error(f"Invalid filter JSON: {e}")
            logger.error("Invalid filter JSON: %s", e)
            ctx.exit(1)

    # Determine clusters to refresh
    if cluster:
        if cluster not in config.data.get("clusters", {}):
            print_error(f"Cluster '{cluster}' not found in configuration.")
            available = list(config.data.get("clusters", {}).keys())
            if available:
                console.print(f"Available clusters: {', '.join(available)}")
            logger.error("Cluster '%s' not found in configuration", cluster)
            ctx.exit(1)
        clusters_to_refresh = [cluster]
    elif refresh_all:
        # Apply filter if provided, otherwise get all clusters
        matching_clusters = config.get_clusters(filter_dict)
        clusters_to_refresh = list(matching_clusters.keys())
        if not clusters_to_refresh:
            if filter_dict:
                print_warning(f"No clusters match filter: {filter_str}")
                logger.warning("No clusters match filter: %s", filter_str)
            else:
                print_warning("No clusters configured.")
                logger.warning("No clusters configured")
            ctx.exit(0)
    else:
        print_error("Specify a cluster name or use --all to refresh all clusters.")
        ctx.exit(1)

    workers = effective_workers(parallel_clusters, len(clusters_to_refresh))

    # The CLI owns the database handles; close them even when the run fails
    # or exits non-zero.
    db = ClusterMetadataDB(config=config)
    try:
        history_db = CacheHistoryDB(config=config)
        try:
            console.print(f"\nRefreshing cache for {len(clusters_to_refresh)} cluster(s)...")
            if filter_dict:
                console.print(f"[dim]Filter: {filter_str}[/dim]")
                logger.info(
                    "Refreshing cache for %d cluster(s) with filter: %s",
                    len(clusters_to_refresh),
                    filter_str,
                )
            else:
                logger.info("Refreshing cache for %d cluster(s)", len(clusters_to_refresh))
            if workers > 1:
                console.print(f"[dim]Parallel workers: {workers}[/dim]")
                logger.info("Parallel workers: %d", workers)
            console.print(f"[dim]Log file: {log_file}[/dim]\n")

            parallel = workers > 1
            reporter: _VerboseReporter | _NormalReporter = (
                _VerboseReporter(parallel) if verbose else _NormalReporter(parallel)
            )
            refresher = CacheRefresher(config, db, history_db)
            with reporter:
                summary = refresher.run(clusters_to_refresh, workers=workers, observer=reporter)
            _report_summary(ctx, summary)
        finally:
            history_db.close()
    finally:
        db.close()


class _VerboseClusterSink:
    """Per-cluster verbose progress sink.

    In parallel mode output is captured into a private ``Console`` (written
    from a worker thread) and flushed as one block by the main thread. In
    sequential mode output goes straight to the live console.
    """

    def __init__(self, display: VerboseProgressDisplay, captured: Console | None) -> None:
        self.display = display
        self.captured = captured

    def on_phase(self, info: ProgressInfo) -> None:
        """Forward a collector phase update to the display."""
        self.display.on_progress(info)

    def on_client_unavailable(self, kind: str, error: Exception) -> None:
        """Show that a client could not be built."""
        if self.captured is not None:
            self.captured.print(f"  [dim]{kind} client unavailable: {error}[/dim]")
        else:
            print_warning(f"  [dim]{kind} client unavailable: {error}[/dim]")

    def on_collection_finished(self, success: bool) -> None:
        """Print the cluster summary into the captured block (parallel only)."""
        if self.captured is not None:
            self.display.print_summary(success=success)

    def captured_text(self) -> str:
        """Return the captured output, or an empty string when not buffering."""
        if self.captured is None:
            return ""
        return self.captured.export_text(clear=False)


class _NormalReporter:
    """Normal-mode rendering: spinner (sequential) and one line per cluster."""

    def __init__(self, parallel: bool) -> None:
        self.parallel = parallel
        self._progress: Progress | None = None
        self._tasks: dict[str, TaskID] = {}

    def __enter__(self) -> _NormalReporter:
        if not self.parallel:
            self._progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            )
            self._progress.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if self._progress is not None:
            self._progress.__exit__(exc_type, exc, tb)
            self._progress = None

    def cluster_started(self, name: str, index: int, total: int) -> ClusterProgress | None:
        """Add a spinner task for the cluster (sequential only)."""
        if self._progress is not None:
            self._tasks[name] = self._progress.add_task(
                f"Collecting metadata for {name}...", total=1
            )
        return None

    def cluster_finished(
        self,
        result: ClusterRefreshResult,
        progress: ClusterProgress | None,
        completed: int,
        total: int,
    ) -> None:
        """Print the cluster's outcome line."""
        name = result.cluster_name
        err = result.error or RuntimeError("Unknown collection failure")
        if result.status is RefreshStatus.OK:
            print_success(f"  {name}: Cache refreshed")
        elif result.status is RefreshStatus.NO_CLIENTS:
            print_error(f"  No clients available for {name}")
        elif result.status is RefreshStatus.PERSIST_FAILED and self.parallel:
            print_exception(f"  {name}: Persist failed - {err}", err)
        else:
            print_exception(f"  {name}: Failed - {err}", err)
        if self._progress is not None and name in self._tasks:
            self._progress.update(self._tasks[name], completed=1)


class _VerboseReporter:
    """Verbose-mode rendering: phase-by-phase progress per cluster."""

    def __init__(self, parallel: bool) -> None:
        self.parallel = parallel
        self._displays: dict[str, VerboseProgressDisplay] = {}

    def __enter__(self) -> _VerboseReporter:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None

    def cluster_started(self, name: str, index: int, total: int) -> ClusterProgress | None:
        """Create the cluster's progress sink (header printed now if sequential)."""
        if not self.parallel:
            display = VerboseProgressDisplay(
                console=console, cluster_name=name, cluster_index=index, total_clusters=total
            )
            display.print_header()
            self._displays[name] = display
            return _VerboseClusterSink(display, None)
        # Write to a private StringIO so workers never touch sys.stdout and
        # race with each other; the main thread replays the block on completion.
        captured = Console(record=True, force_terminal=False, width=120, file=io.StringIO())
        display = VerboseProgressDisplay(
            console=captured,
            cluster_name=name,
            cluster_index=0,
            total_clusters=0,
            buffered=True,
        )
        return _VerboseClusterSink(display, captured)

    def cluster_finished(
        self,
        result: ClusterRefreshResult,
        progress: ClusterProgress | None,
        completed: int,
        total: int,
    ) -> None:
        """Render the cluster's outcome."""
        name = result.cluster_name
        err = result.error or RuntimeError("Unknown collection failure")
        if self.parallel:
            console.print(f"\n[bold][{completed}/{total}] {name}[/bold]")
            if isinstance(progress, _VerboseClusterSink):
                text = progress.captured_text()
                if text:
                    # Captured output already ends with newlines.
                    console.out(text, end="", highlight=False)
            if result.status is RefreshStatus.NO_CLIENTS:
                print_error(f"  No clients available for {name}")
            elif result.status is RefreshStatus.COLLECT_FAILED:
                print_exception(f"  Error: {err}", err)
            elif result.status is RefreshStatus.PERSIST_FAILED:
                print_exception(f"  Persist failed: {err}", err)
            return

        display = self._displays.pop(name)
        if result.status is RefreshStatus.OK:
            display.print_summary(True)
        elif result.status is RefreshStatus.NO_CLIENTS:
            print_error(f"  No clients available for {name}")
            display.print_summary(False)
        else:
            display.print_summary(success=False)
            print_exception(f"  Error: {err}", err)


def _print_failure_summary(
    failures: dict[str, list[str]],
) -> None:
    """Print a per-cluster failure summary.

    Args:
        failures: Dict mapping cluster name to list of failure descriptions.
    """
    if not failures:
        return

    console.print("\n[bold red]Failure Summary:[/bold red]")
    for cluster_name, messages in failures.items():
        console.print(f"  {cluster_name}:")
        for msg in messages:
            console.print(f"    {msg}")


def _report_summary(ctx: click.Context, summary: RefreshSummary) -> None:
    """Print the final counts and exit non-zero when any cluster failed."""
    success_count = summary.succeeded
    error_count = summary.failed
    console.print()
    if success_count > 0:
        print_success(f"Successfully refreshed {success_count} cluster(s)")
    if error_count > 0:
        print_error(f"Failed to refresh {error_count} cluster(s)")
        _print_failure_summary(summary.failures)
        logger.error("Failed to refresh %d cluster(s)", error_count)
        ctx.exit(1)

    logger.info("Cache refresh completed: %d success, %d failed", success_count, error_count)
