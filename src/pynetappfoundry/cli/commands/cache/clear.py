"""Cache clear command."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.options import all_option
from pynetappfoundry.cli.utils import print_success, print_warning
from pynetappfoundry.core.config import Config

console = Console()


@click.command()
@click.argument("cluster", required=False)
@all_option(param_name="clear_all", help_text="Clear cache for all clusters.", short_flag=True)
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
        raise CliError(f"Configuration directory not found: {config_path}")

    try:
        config = Config(config_dir=config_dir, script_name="cache-clear")
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}", exc=e) from e

    if not cluster and not clear_all:
        raise CliError("Specify a cluster name or use --all to clear all cached data.")

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
                console.print(f"  - {escape(str(c['cluster_name']))}")
            if not click.confirm("Proceed?"):
                console.print("Cancelled.")
                db.close()
                ctx.exit(0)

        deleted = db.clear()
        db.close()

        print_success(f"Cleared cache for {deleted} cluster(s).")
