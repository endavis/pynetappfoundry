"""AIQUM cache commands: refresh, status and clear (#1072, ADR-0026)."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from pynetappfoundry.cache import AiqumCacheDB, refresh_aiqum_cache
from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.options import all_option
from pynetappfoundry.cli.utils import print_error, print_success, print_warning
from pynetappfoundry.core.config import Config, ConfigurationError

console = Console()


def _load_config(ctx: click.Context, script_name: str) -> Config:
    """Load the configuration for an AIQUM cache command."""
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        raise CliError(f"Configuration directory not found: {config_path}")
    try:
        return Config(config_dir=config_dir, script_name=script_name)
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}", exc=e) from e


def _configured(config: Config) -> set[str]:
    """Return the names in the ``[aiqums]`` inventory."""
    return set(config.data.get("aiqums", {}))


@click.group()
def aiqum() -> None:
    """AIQUM cache management.

    Commands for refreshing, inspecting and clearing the local cache of
    collected AIQUM collections.
    """


@aiqum.command()
@click.argument("instance", required=False)
@all_option(
    param_name="refresh_all", help_text="Refresh every configured AIQUM instance.", short_flag=True
)
@click.pass_context
def refresh(ctx: click.Context, instance: str | None, refresh_all: bool) -> None:
    """Collect AIQUM instances and replace their cached snapshots.

    Examples:

        nf cache aiqum refresh aiq1    # Refresh one instance
        nf cache aiqum refresh --all   # Refresh every configured instance
    """
    # Deferred: importing the collector runner loads the ONTAP models, which
    # `nf --help` must not pay for (#960).
    from pynetappfoundry.cache._collector_runner import CollectionError

    config = _load_config(ctx, "cache-aiqum-refresh")
    if not instance and not refresh_all:
        raise CliError("Specify an AIQUM instance or use --all.")

    targets = [instance] if instance else sorted(_configured(config))
    if not targets:
        print_warning("No AIQUM instances are configured.")
        ctx.exit(0)

    failed: list[str] = []
    with AiqumCacheDB(config=config) as db:
        for name in targets:
            try:
                snapshot = refresh_aiqum_cache(config, name, db=db)
            except (CollectionError, ConfigurationError, ValueError) as e:
                print_error(f"AIQUM '{escape(name)}': {escape(str(e))}")
                failed.append(name)
                continue
            counts = ", ".join(f"{m}: {len(r)}" for m, r in sorted(snapshot.records.items()))
            print_success(f"Refreshed AIQUM '{escape(name)}' ({escape(counts)}).")

    if failed:
        raise CliError(f"Refresh failed for: {', '.join(failed)}")


@aiqum.command()
@click.option(
    "--ttl",
    "-t",
    type=int,
    default=30,
    help="Days before cache is considered stale (default: 30).",
)
@click.pass_context
def status(ctx: click.Context, ttl: int) -> None:
    """Show the AIQUM cache status per instance and mapping.

    Examples:

        nf cache aiqum status           # Show status with default TTL
        nf cache aiqum status --ttl 7   # Consider stale after 7 days
    """
    config = _load_config(ctx, "cache-aiqum-status")
    configured = _configured(config)

    with AiqumCacheDB(config=config) as db:
        cached = set(db.list_instances())
        table = Table(title="AIQUM Cache Status")
        table.add_column("Instance")
        table.add_column("Mapping")
        table.add_column("Cached At")
        table.add_column("Status")

        stale_count = 0
        for name in sorted(configured | cached):
            rows = db.list_collections(name)
            if not rows:
                table.add_row(escape(name), "-", "-", "[yellow]Not cached[/yellow]")
                continue
            if name not in configured:
                label = "[dim]Orphaned[/dim]"
            elif db.is_stale(name, ttl):
                label = "[red]Stale[/red]"
                stale_count += 1
            else:
                label = "[green]Fresh[/green]"
            for row in rows:
                table.add_row(escape(name), escape(row["mapping"]), escape(row["cached_at"]), label)

    console.print()
    console.print(table)
    console.print()
    console.print("[bold]Summary:[/bold]")
    console.print(f"  Configured instances: {len(configured)}")
    console.print(f"  Cached: {len(cached & configured)}")
    console.print(f"  Stale (>{ttl} days): {stale_count}")
    console.print()


@aiqum.command()
@click.argument("instance", required=False)
@all_option(param_name="clear_all", help_text="Clear the cache for all instances.", short_flag=True)
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt.")
@click.pass_context
def clear(ctx: click.Context, instance: str | None, clear_all: bool, force: bool) -> None:
    """Clear the AIQUM cache.

    Examples:

        nf cache aiqum clear aiq1     # Clear one instance
        nf cache aiqum clear --all -f # Clear everything without confirmation
    """
    config = _load_config(ctx, "cache-aiqum-clear")
    if not instance and not clear_all:
        raise CliError("Specify an AIQUM instance or use --all to clear all cached data.")

    with AiqumCacheDB(config=config) as db:
        cached = db.list_instances()
        if instance:
            if instance not in cached:
                print_warning(f"No cached data found for AIQUM '{escape(instance)}'.")
                ctx.exit(0)
            if not force and not click.confirm(f"Clear cache for AIQUM '{instance}'?"):
                console.print("Cancelled.")
                ctx.exit(0)
            db.clear(instance)
            print_success(f"Cleared AIQUM cache for '{escape(instance)}'.")
            return

        if not cached:
            print_warning("No cached data found.")
            ctx.exit(0)
        if not force:
            console.print(f"This will clear the cache for {len(cached)} instance(s):")
            for name in cached:
                console.print(f"  - {escape(name)}")
            if not click.confirm("Proceed?"):
                console.print("Cancelled.")
                ctx.exit(0)
        db.clear()
        print_success(f"Cleared AIQUM cache for {len(cached)} instance(s).")
