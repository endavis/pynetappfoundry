"""Cache refresh command."""

from __future__ import annotations

import contextlib
import logging
import time
from datetime import UTC, datetime
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pynetappfoundry.cache import (
    ClusterMetadataDB,
    CollectionPhase,
    MetadataCollector,
    ProgressCallback,
    ProgressInfo,
)
from pynetappfoundry.cli.utils import (
    print_error,
    print_exception,
    print_success,
    print_warning,
)
from pynetappfoundry.clients.ontap import ONTAPCLI, ONTAPAPIClient
from pynetappfoundry.core.config import Config

console = Console()

# Module logger
logger = logging.getLogger(__name__)

# Log directory for cache refresh operations
LOG_DIR = Path.home() / ".cache" / "pynetappfoundry" / "logs"
MAX_LOG_FILES = 10  # Keep last N log files


def setup_file_logging() -> Path:
    """Configure file logging for the cache refresh operation.

    Returns:
        Path to the log file.
    """
    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Create timestamped log file
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    log_file = LOG_DIR / f"cache-refresh-{timestamp}.log"

    # Configure file handler for the cache module
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add handler to cache module loggers
    cache_logger = logging.getLogger("pynetappfoundry.cache")
    cache_logger.setLevel(logging.DEBUG)
    cache_logger.addHandler(file_handler)

    # Also add to this module's logger
    refresh_logger = logging.getLogger(__name__)
    refresh_logger.setLevel(logging.DEBUG)
    refresh_logger.addHandler(file_handler)

    # Clean up old log files
    cleanup_old_logs()

    return log_file


def cleanup_old_logs() -> None:
    """Remove old log files, keeping only the most recent ones."""
    if not LOG_DIR.exists():
        return

    log_files = sorted(
        LOG_DIR.glob("cache-refresh-*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    # Remove files beyond MAX_LOG_FILES
    for old_file in log_files[MAX_LOG_FILES:]:
        try:
            old_file.unlink()
            logger.debug("Removed old log file: %s", old_file)
        except OSError as e:
            logger.warning("Failed to remove old log file %s: %s", old_file, e)


class VerboseProgressDisplay:
    """Displays detailed progress information in verbose mode."""

    def __init__(
        self, console: Console, cluster_name: str, cluster_index: int, total_clusters: int
    ) -> None:
        """Initialize the verbose progress display.

        Args:
            console: Rich console for output.
            cluster_name: Name of the cluster being processed.
            cluster_index: 1-based index of the current cluster.
            total_clusters: Total number of clusters to process.
        """
        self.console = console
        self.cluster_name = cluster_name
        self.cluster_index = cluster_index
        self.total_clusters = total_clusters
        self.phase_times: dict[CollectionPhase, float] = {}
        self.start_time = time.monotonic()
        self.current_phase: CollectionPhase | None = None

    def on_progress(self, info: ProgressInfo) -> None:
        """Handle progress callback from MetadataCollector.

        Args:
            info: Progress information for the current phase.
        """
        if info.status == "starting":
            self.current_phase = info.phase
            # Print phase starting (will be overwritten or followed by completion)
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
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed progress for each collection phase.",
)
@click.pass_context
def refresh(ctx: click.Context, cluster: str | None, refresh_all: bool, verbose: bool) -> None:
    """Refresh the metadata cache for cluster(s).

    If CLUSTER is specified, refresh only that cluster.
    Use --all to refresh all configured clusters.

    Examples:

        nf cache refresh cluster1      # Refresh single cluster
        nf cache refresh --all         # Refresh all clusters
        nf cache refresh --all -v      # Refresh all with detailed progress
    """
    # Always set up file logging
    log_file = setup_file_logging()
    logger.info("Starting cache refresh operation")

    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        logger.error("Configuration directory not found: %s", config_path)
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-refresh")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        logger.exception("Failed to load configuration")
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
        clusters_to_refresh = list(config.data.get("clusters", {}).keys())
        if not clusters_to_refresh:
            print_warning("No clusters configured.")
            logger.warning("No clusters configured")
            ctx.exit(0)
    else:
        print_error("Specify a cluster name or use --all to refresh all clusters.")
        ctx.exit(1)

    # Initialize cache database
    db = ClusterMetadataDB(config=config)

    console.print(f"\nRefreshing cache for {len(clusters_to_refresh)} cluster(s)...")
    console.print(f"[dim]Log file: {log_file}[/dim]\n")
    logger.info("Refreshing cache for %d cluster(s)", len(clusters_to_refresh))

    if verbose:
        # Verbose mode: detailed phase-by-phase progress
        _refresh_verbose(ctx, config, db, clusters_to_refresh)
    else:
        # Normal mode: spinner per cluster
        _refresh_normal(ctx, config, db, clusters_to_refresh)

    db.close()


def _refresh_normal(
    ctx: click.Context,
    config: Config,
    db: ClusterMetadataDB,
    clusters_to_refresh: list[str],
) -> None:
    """Refresh clusters with spinner progress (normal mode).

    Args:
        ctx: Click context.
        config: Configuration object.
        db: Cache database.
        clusters_to_refresh: List of cluster names.
    """
    success_count = 0
    error_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for cluster_name in clusters_to_refresh:
            task = progress.add_task(f"Collecting metadata for {cluster_name}...", total=1)
            logger.info("Processing cluster: %s", cluster_name)

            try:
                success = _process_cluster(config, db, cluster_name, verbose=False)
                if success:
                    print_success(f"  {cluster_name}: Cache refreshed")
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                print_exception(f"  {cluster_name}: Failed - {e}", e)
                logger.exception("Failed to process cluster %s", cluster_name)
                error_count += 1

            progress.update(task, completed=1)

    # Summary
    console.print()
    if success_count > 0:
        print_success(f"Successfully refreshed {success_count} cluster(s)")
    if error_count > 0:
        print_error(f"Failed to refresh {error_count} cluster(s)")
        logger.error("Failed to refresh %d cluster(s)", error_count)
        ctx.exit(1)

    logger.info("Cache refresh completed: %d success, %d failed", success_count, error_count)


def _refresh_verbose(
    ctx: click.Context,
    config: Config,
    db: ClusterMetadataDB,
    clusters_to_refresh: list[str],
) -> None:
    """Refresh clusters with detailed progress (verbose mode).

    Args:
        ctx: Click context.
        config: Configuration object.
        db: Cache database.
        clusters_to_refresh: List of cluster names.
    """
    success_count = 0
    error_count = 0
    total_clusters = len(clusters_to_refresh)

    for idx, cluster_name in enumerate(clusters_to_refresh, 1):
        logger.info("Processing cluster: %s (%d/%d)", cluster_name, idx, total_clusters)

        display = VerboseProgressDisplay(
            console=console,
            cluster_name=cluster_name,
            cluster_index=idx,
            total_clusters=total_clusters,
        )
        display.print_header()

        try:
            success = _process_cluster(
                config, db, cluster_name, verbose=True, progress_callback=display.on_progress
            )
            display.print_summary(success)
            if success:
                success_count += 1
            else:
                error_count += 1

        except Exception as e:
            display.print_summary(success=False)
            print_exception(f"  Error: {e}", e)
            logger.exception("Failed to process cluster %s", cluster_name)
            error_count += 1

    # Summary
    console.print()
    if success_count > 0:
        print_success(f"Successfully refreshed {success_count} cluster(s)")
    if error_count > 0:
        print_error(f"Failed to refresh {error_count} cluster(s)")
        logger.error("Failed to refresh %d cluster(s)", error_count)
        ctx.exit(1)

    logger.info("Cache refresh completed: %d success, %d failed", success_count, error_count)


def _process_cluster(
    config: Config,
    db: ClusterMetadataDB,
    cluster_name: str,
    verbose: bool = False,
    progress_callback: ProgressCallback | None = None,
) -> bool:
    """Process a single cluster for cache refresh.

    Args:
        config: Configuration object.
        db: Cache database.
        cluster_name: Name of the cluster.
        verbose: Whether verbose mode is enabled.
        progress_callback: Optional callback for progress updates.

    Returns:
        True if successful, False otherwise.
    """
    cluster_data = config.data["clusters"][cluster_name]

    # Get credentials
    user, password = config.get_user("clusters", cluster_name)

    # Create cluster object for API client
    class ClusterObj:
        def __init__(self, name: str, ip: str) -> None:
            self.name = name
            self.ip = ip

    cluster_obj = ClusterObj(cluster_name, cluster_data.get("ip", ""))

    # Initialize clients
    api_client: ONTAPAPIClient | None = None
    cli_client: ONTAPCLI | None = None

    try:
        api_client = ONTAPAPIClient(cluster=cluster_obj, config=config)
        logger.debug("API client initialized for %s", cluster_name)
    except Exception as e:
        if verbose:
            print_warning(f"  [dim]API client unavailable: {e}[/dim]")
        logger.warning("API client unavailable for %s: %s", cluster_name, e)

    try:
        cli_client = ONTAPCLI(
            name=cluster_name,
            host_or_ip=cluster_data.get("ip", ""),
            username=user,
            password=password,
        )
        logger.debug("CLI client initialized for %s", cluster_name)
    except Exception as e:
        if verbose:
            print_warning(f"  [dim]CLI client unavailable: {e}[/dim]")
        logger.warning("CLI client unavailable for %s: %s", cluster_name, e)

    if not api_client and not cli_client:
        print_error(f"  No clients available for {cluster_name}")
        logger.error("No clients available for %s", cluster_name)
        return False

    # Collect metadata
    collector = MetadataCollector(
        api_client=api_client,
        cli_client=cli_client,
        progress_callback=progress_callback,
    )
    metadata = collector.collect_all(cluster_name)

    # Store in cache
    db.set(cluster_name, metadata)
    logger.info("Cache updated for %s", cluster_name)

    # Clean up CLI client
    if cli_client:
        with contextlib.suppress(Exception):
            cli_client.disconnect()
            logger.debug("CLI client disconnected for %s", cluster_name)

    return True
