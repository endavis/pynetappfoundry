"""OCCM (Console agent) cache commands (#1087, ADR-0030)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from pynetappfoundry.cache import OccmCacheDB, refresh_occm_cache
from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.options import all_option
from pynetappfoundry.cli.utils import print_success, print_warning
from pynetappfoundry.core.config import Config, ConfigurationError

console = Console()


def _load_config(ctx: click.Context, script_name: str) -> Config:
    """Load the configuration from the CLI's config directory."""
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        raise CliError(f"Configuration directory not found: {config_path}")
    try:
        return Config(config_dir=config_dir, script_name=script_name)
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}", exc=e) from e


@click.group()
def occm() -> None:
    """Console agent (OCCM) cache management.

    Commands for refreshing and inspecting the local cache of what the
    Console agents report: their working environments and which agents
    manage each one.

    Examples:

        nf cache occm refresh                 # Discover and collect every account
        nf cache occm status                  # Show per-agent cache status
        nf cache occm agents WE_PUBLIC_ID     # Agents managing a working environment
    """
    pass


@occm.command("refresh")
@click.option(
    "--scope",
    "-s",
    help="Refresh only this configured Console account scope (default: every account).",
)
@click.pass_context
def refresh(ctx: click.Context, scope: str | None) -> None:
    """Discover the Console agents and refresh the OCCM cache.

    Examples:

        nf cache occm refresh                 # Every configured account
        nf cache occm refresh --scope prod    # One account
    """
    config = _load_config(ctx, "cache-occm")

    if scope:
        try:
            available = config.console_account_scopes()
        except ConfigurationError as e:
            raise CliError(f"Failed to read the Console accounts: {e}", exc=e) from e
        names = sorted(s for s in available if s is not None)
        if scope not in names:
            listed = ", ".join(names) if names else "none"
            raise CliError(
                f"Unknown Console scope '{scope}'.", hints=[f"Available scopes: {escape(listed)}"]
            )

    try:
        snapshot = refresh_occm_cache(config, scopes=(scope,) if scope else None)
    except Exception as e:
        raise CliError(f"OCCM discovery failed: {e}", exc=e) from e

    table = Table(title="Collected Agents")
    table.add_column("Agent", style="cyan")
    table.add_column("Scope")
    table.add_column("Records", justify="right")
    for agent in snapshot.agents:
        table.add_row(
            escape(agent.agent_id),
            escape(agent.scope or "(root)"),
            str(sum(len(v) for v in agent.records.values())),
        )
    console.print()
    if snapshot.agents:
        console.print(table)
    else:
        console.print("No agents collected.")

    for agent_id in snapshot.skipped_agents:
        print_warning(f"Agent '{escape(agent_id)}' skipped: not active.")
    for agent_id, mapping in snapshot.failed_mappings:
        print_warning(f"Agent '{escape(agent_id)}': mapping {escape(mapping)} failed.")
    for agent_id in snapshot.failed_agents:
        print_warning(f"Agent '{escape(agent_id)}' failed.")

    if snapshot.failed_agents:
        raise CliError(
            f"OCCM refresh finished with {len(snapshot.failed_agents)} failed agent(s); "
            "their earlier cached rows were kept."
        )
    print_success(f"Refreshed {len(snapshot.agents)} agent(s).")


@occm.command("status")
@click.option(
    "--ttl",
    "-t",
    type=int,
    default=30,
    help="Days before an agent's cache is considered stale (default: 30).",
)
@click.pass_context
def status(ctx: click.Context, ttl: int) -> None:
    """Show the OCCM cache status for every agent.

    Examples:

        nf cache occm status           # Default TTL
        nf cache occm status --ttl 7   # Stale after 7 days
    """
    config = _load_config(ctx, "cache-occm")
    with OccmCacheDB(config=config) as db:
        statuses = {s.agent_id: s for s in db.agent_status(ttl_days=ttl)}
        inventory = db.agents()

    if not statuses and not inventory:
        print_warning("No OCCM cache data found.")
        console.print("Run 'nf cache occm refresh' to populate it.")
        ctx.exit(0)

    table = Table(title="OCCM Cache Status")
    table.add_column("Agent", style="cyan")
    table.add_column("Name")
    table.add_column("Scope")
    table.add_column("Discovery status")
    table.add_column("Mappings", justify="right")
    table.add_column("Records", justify="right")
    table.add_column("Cached at (oldest)")
    table.add_column("Age (days)", justify="right")
    table.add_column("State", justify="center")

    now = datetime.now(UTC)
    fresh = stale = missing = 0
    seen: set[str] = set()

    def add_row(
        agent_id: str, name: str | None, scope: str | None, discovery_status: str | None
    ) -> None:
        nonlocal fresh, stale, missing
        seen.add(agent_id)
        st = statuses.get(agent_id)
        if st is None:
            missing += 1
            cells = ["-", "-", "-", "-", "[yellow]Not collected[/yellow]"]
        else:
            age = (now - st.oldest_cached_at).days
            if st.is_stale:
                stale += 1
                state = "[red]Stale[/red]"
            else:
                fresh += 1
                state = "[green]Fresh[/green]"
            cells = [
                str(st.mapping_count),
                str(st.record_count),
                st.oldest_cached_at.isoformat()[:19],
                str(age),
                state,
            ]
        table.add_row(
            escape(agent_id),
            escape(name or "-"),
            escape(scope or "(root)"),
            escape(discovery_status or "-"),
            *cells,
        )

    for info in inventory:
        add_row(info.agent_id, info.name, info.scope, info.status)
    for agent_id, st in statuses.items():
        if agent_id not in seen:
            add_row(agent_id, None, st.scope, None)

    console.print()
    console.print(table)
    console.print(f"\n{fresh} fresh, {stale} stale, {missing} not collected (TTL {ttl} days)\n")


@occm.command("agents")
@click.argument("public_id", required=False)
@click.pass_context
def agents(ctx: click.Context, public_id: str | None) -> None:
    """Show which agents manage working environments.

    With PUBLIC_ID, list the agents that manage that working environment.
    Without it, list every working environment and its agents.

    Examples:

        nf cache occm agents                 # Every working environment
        nf cache occm agents WE_PUBLIC_ID    # One working environment
    """
    config = _load_config(ctx, "cache-occm")
    with OccmCacheDB(config=config) as db:
        if public_id:
            found = db.agents_for_working_environment(public_id)
            if not found:
                raise CliError(f"No cached agent manages working environment '{public_id}'.")
            console.print(f"Working environment {escape(public_id)}:")
            for agent_id in found:
                console.print(f"  - {escape(agent_id)}")
            return
        mapping = db.working_environment_agents()

    if not mapping:
        print_warning("No working environments cached.")
        console.print("Run 'nf cache occm refresh' to populate the cache.")
        ctx.exit(0)

    table = Table(title="Working Environments")
    table.add_column("Working environment", style="cyan")
    table.add_column("Agents")
    for we_id, agent_ids in mapping.items():
        table.add_row(escape(we_id), escape(", ".join(agent_ids)))
    console.print()
    console.print(table)
    console.print()


@occm.command("clear")
@click.argument("agent_id", required=False)
@all_option(param_name="clear_all", help_text="Clear the whole OCCM cache.", short_flag=True)
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt.")
@click.pass_context
def clear(ctx: click.Context, agent_id: str | None, clear_all: bool, force: bool) -> None:
    """Clear the OCCM cache.

    If AGENT_ID is given, clear only that agent's cached rows.
    Use --all to clear everything, including the discovery inventory.

    Examples:

        nf cache occm clear AGENT_ID     # One agent
        nf cache occm clear --all -f     # Everything, no prompt
    """
    config = _load_config(ctx, "cache-occm")
    if not agent_id and not clear_all:
        raise CliError("Specify an agent id or use --all to clear all OCCM cache data.")

    with OccmCacheDB(config=config) as db:
        if agent_id:
            if agent_id not in db.list_agents():
                print_warning(f"No cached data found for agent '{agent_id}'.")
                ctx.exit(0)
            if not force and not click.confirm(f"Clear cache for agent '{agent_id}'?"):
                console.print("Cancelled.")
                ctx.exit(0)
            deleted = db.clear(agent_id)
            print_success(f"Cleared {deleted} record(s) for agent '{agent_id}'.")
            return

        if not force and not click.confirm("Clear the whole OCCM cache?"):
            console.print("Cancelled.")
            ctx.exit(0)
        deleted = db.clear()
        print_success(f"Cleared the OCCM cache ({deleted} record(s)).")
