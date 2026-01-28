"""Cache status command."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cli.utils import print_error, print_exception, print_warning
from pynetappfoundry.core.config import Config

console = Console()


@click.command()
@click.option(
    "--ttl",
    "-t",
    type=int,
    default=30,
    help="Days before cache is considered stale (default: 30).",
)
@click.pass_context
def status(ctx: click.Context, ttl: int) -> None:
    """Show cache status for all clusters.

    Displays which clusters have cached data and whether
    the cache is stale.

    Examples:

        nf cache status           # Show status with default TTL
        nf cache status --ttl 7   # Consider stale after 7 days
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-status")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    db = ClusterMetadataDB(config=config)

    # Get configured clusters
    configured_clusters = set(config.data.get("clusters", {}).keys())

    # Get cache status
    cache_status = db.get_status(ttl_days=ttl)
    cached_clusters: set[str] = {str(s["cluster_name"]) for s in cache_status}

    db.close()

    # Build status table
    table = Table(title="Cache Status")
    table.add_column("Cluster", style="cyan")
    table.add_column("Cached", justify="center")
    table.add_column("Age (days)", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Cache Version")

    # Map cache status by cluster name
    status_by_name = {str(s["cluster_name"]): s for s in cache_status}

    # Show all configured clusters
    for cluster in sorted(configured_clusters):
        if cluster in status_by_name:
            s = status_by_name[cluster]
            age_days = s.get("age_days", 0)
            is_stale = s.get("is_stale", False)
            status_str = "[red]Stale[/red]" if is_stale else "[green]Fresh[/green]"
            table.add_row(
                cluster,
                "[green]Yes[/green]",
                str(age_days),
                status_str,
                str(s.get("cache_version", "")),
            )
        else:
            table.add_row(
                cluster,
                "[yellow]No[/yellow]",
                "-",
                "[yellow]Not cached[/yellow]",
                "-",
            )

    # Check for orphaned cache entries (cached but not configured)
    orphaned: set[str] = cached_clusters - configured_clusters
    if orphaned:
        for cluster in sorted(orphaned):
            s = status_by_name[cluster]
            age_days = s.get("age_days", 0)
            table.add_row(
                cluster,
                "[green]Yes[/green]",
                str(age_days),
                "[dim]Orphaned[/dim]",
                str(s.get("cache_version", "")),
            )

    console.print()
    console.print(table)

    # Summary
    total_configured = len(configured_clusters)
    total_cached = len(cached_clusters & configured_clusters)
    stale_count = sum(
        1
        for s in cache_status
        if s["cluster_name"] in configured_clusters and s.get("is_stale", False)
    )

    console.print()
    console.print("[bold]Summary:[/bold]")
    console.print(f"  Configured clusters: {total_configured}")
    console.print(f"  Cached: {total_cached}")
    console.print(f"  Stale (>{ttl} days): {stale_count}")
    if orphaned:
        print_warning(f"  Orphaned cache entries: {len(orphaned)}")
    console.print()

    if total_cached < total_configured:
        uncached = configured_clusters - cached_clusters
        print_warning(
            f"Missing cache for: {', '.join(sorted(uncached)[:5])}"
            + (f" and {len(uncached) - 5} more" if len(uncached) > 5 else "")
        )
        console.print("Run 'nf cache refresh --all' to populate the cache.")
