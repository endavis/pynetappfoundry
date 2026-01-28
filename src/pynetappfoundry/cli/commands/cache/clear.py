"""Cache clear command."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cli.utils import print_error, print_exception, print_success, print_warning
from pynetappfoundry.core.config import Config

console = Console()


@click.command()
@click.argument("cluster", required=False)
@click.option(
    "--all",
    "-a",
    "clear_all",
    is_flag=True,
    help="Clear cache for all clusters.",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Skip confirmation prompt.",
)
@click.pass_context
def clear(ctx: click.Context, cluster: str | None, clear_all: bool, force: bool) -> None:
    """Clear the metadata cache.

    If CLUSTER is specified, clear only that cluster's cache.
    Use --all to clear all cached data.

    Examples:

        nf cache clear cluster1      # Clear single cluster
        nf cache clear --all         # Clear all cached data
        nf cache clear --all -f      # Clear all without confirmation
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-clear")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    if not cluster and not clear_all:
        print_error("Specify a cluster name or use --all to clear all cached data.")
        ctx.exit(1)

    db = ClusterMetadataDB(config=config)

    if cluster:
        # Check if cluster exists in cache
        cached = db.get(cluster)
        if not cached:
            print_warning(f"No cached data found for cluster '{cluster}'.")
            db.close()
            ctx.exit(0)

        if not force and not click.confirm(f"Clear cache for cluster '{cluster}'?"):
            console.print("Cancelled.")
            db.close()
            ctx.exit(0)

        deleted = db.clear(cluster)
        db.close()

        if deleted > 0:
            print_success(f"Cleared cache for cluster '{cluster}'.")
        else:
            print_warning(f"No cache entry found for '{cluster}'.")

    else:
        # Clear all
        clusters = db.list_clusters()
        if not clusters:
            print_warning("No cached data found.")
            db.close()
            ctx.exit(0)

        if not force:
            console.print(f"This will clear cache for {len(clusters)} cluster(s):")
            for c in clusters:
                console.print(f"  - {c['cluster_name']}")
            if not click.confirm("Proceed?"):
                console.print("Cancelled.")
                db.close()
                ctx.exit(0)

        deleted = db.clear()
        db.close()

        print_success(f"Cleared cache for {deleted} cluster(s).")
