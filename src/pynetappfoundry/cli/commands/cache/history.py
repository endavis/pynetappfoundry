"""Cache history commands for viewing change tracking."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pynetappfoundry.cache import CacheHistoryDB, format_diff_summary, is_schema_compatible
from pynetappfoundry.cli.utils import print_error, print_exception, print_warning
from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)
console = Console()


@click.group()
def history() -> None:
    """View cache change history.

    Commands for viewing the history of metadata changes
    recorded during cache refresh operations.

    Examples:

        nf cache history list cluster1     # List changes for a cluster
        nf cache history show 5            # Show full details of change #5
        nf cache history diff 5            # Show formatted diff for change #5
    """
    pass


@history.command("list")
@click.argument("cluster", required=False)
@click.option(
    "--limit",
    "-n",
    type=int,
    default=20,
    help="Maximum number of records to show (default: 20).",
)
@click.option(
    "--offset",
    type=int,
    default=0,
    help="Number of records to skip.",
)
@click.option(
    "--since",
    help="Filter changes after this date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).",
)
@click.option(
    "--until",
    help="Filter changes before this date (ISO format).",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.pass_context
def list_history(
    ctx: click.Context,
    cluster: str | None,
    limit: int,
    offset: int,
    since: str | None,
    until: str | None,
    output_json: bool,
) -> None:
    """List change history events.

    If CLUSTER is specified, shows history for that cluster only.
    Otherwise shows history for all clusters.

    Examples:

        nf cache history list                      # All clusters
        nf cache history list cluster1             # Specific cluster
        nf cache history list -n 50                # Show 50 records
        nf cache history list --since 2024-01-01   # Changes since date
    """
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-history")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    db = CacheHistoryDB(config=config)

    try:
        records = db.get_change_history(
            cluster_name=cluster,
            limit=limit,
            offset=offset,
            since=since,
            until=until,
        )
        total = db.get_history_count(cluster_name=cluster)
    except ValueError as e:
        db.close()
        print_error(f"Invalid cluster name: {e}")
        ctx.exit(1)

    db.close()

    if output_json:
        console.print(json.dumps(records, indent=2, default=str))
        return

    if not records:
        if cluster:
            print_warning(f"No change history found for cluster '{cluster}'.")
        else:
            print_warning("No change history found.")
        console.print("Run 'nf cache refresh' to create history entries.")
        ctx.exit(0)

    # Build table
    table = Table(title="Cache Change History")
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Cluster", style="cyan")
    table.add_column("Changed At")
    table.add_column("Summary", style="dim")

    for record in records:
        summary_raw = record.get("summary", [])
        summary: list[dict[str, object]] = summary_raw if isinstance(summary_raw, list) else []
        summary_str = _format_summary_brief(summary)
        table.add_row(
            str(record["id"]),
            str(record["cluster_name"]),
            str(record["changed_at"])[:19],  # Trim microseconds
            summary_str,
        )

    console.print()
    console.print(table)

    # Pagination info
    showing_end = offset + len(records)
    console.print(f"\n[dim]Showing {offset + 1}-{showing_end} of {total} records[/dim]")
    if showing_end < total:
        console.print(f"[dim]Use --offset {showing_end} to see more[/dim]")
    console.print()


@history.command("show")
@click.argument("change_id", type=int)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.pass_context
def show_change(
    ctx: click.Context,
    change_id: int,
    output_json: bool,
) -> None:
    """Show full details of a specific change.

    Displays the complete before and after JSON snapshots
    along with the change summary.

    Examples:

        nf cache history show 5           # Show change #5
        nf cache history show 5 --json    # Output as JSON
    """
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-history")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    db = CacheHistoryDB(config=config)
    record = db.get_change_by_id(change_id)
    db.close()

    if not record:
        print_error(f"Change record #{change_id} not found.")
        ctx.exit(1)

    if output_json:
        # Parse the JSON strings so they're nested properly in output
        before_json = record.get("before_json")
        after_json = record.get("after_json")
        output = {
            "id": record["id"],
            "cluster_name": record["cluster_name"],
            "changed_at": record["changed_at"],
            "summary": record["summary"],
            "before": json.loads(str(before_json)) if before_json else None,
            "after": json.loads(str(after_json)) if after_json else None,
        }
        console.print(json.dumps(output, indent=2, default=str))
        return

    # Display formatted output
    console.print()
    console.print(f"[bold]Change #{record['id']}[/bold]")
    console.print(f"[cyan]Cluster:[/cyan] {record['cluster_name']}")
    console.print(f"[cyan]Changed at:[/cyan] {record['changed_at']}")
    console.print()

    # Summary
    summary_raw = record.get("summary", [])
    summary: list[dict[str, object]] = summary_raw if isinstance(summary_raw, list) else []
    if summary:
        console.print("[bold]Summary:[/bold]")
        console.print(format_diff_summary(summary))
        console.print()

    # Before/After info
    before_json = record.get("before_json")
    if before_json:
        console.print(
            Panel(
                "[dim]Use --json flag to see full snapshot data[/dim]",
                title="Before Snapshot",
                border_style="yellow",
            )
        )
    else:
        console.print("[yellow]No 'before' snapshot (initial capture)[/yellow]")

    console.print(
        Panel(
            "[dim]Use --json flag to see full snapshot data[/dim]",
            title="After Snapshot",
            border_style="green",
        )
    )
    console.print()


@history.command("diff")
@click.argument("change_id", type=int)
@click.option(
    "--category",
    "-c",
    help="Filter to specific category (e.g., 'nodes', 'storage.aggregates').",
)
@click.pass_context
def show_diff(
    ctx: click.Context,
    change_id: int,
    category: str | None,
) -> None:
    """Show formatted diff for a specific change.

    Displays a human-readable summary of what changed,
    organized by change type (added, removed, modified).

    Examples:

        nf cache history diff 5                      # Show all changes
        nf cache history diff 5 -c nodes             # Filter to nodes only
        nf cache history diff 5 -c storage.aggregates  # Filter to aggregates
    """
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-history")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    db = CacheHistoryDB(config=config)
    record = db.get_change_by_id(change_id)
    db.close()

    if not record:
        print_error(f"Change record #{change_id} not found.")
        ctx.exit(1)

    console.print()
    console.print(f"[bold]Change #{record['id']} - {record['cluster_name']}[/bold]")
    console.print(f"[dim]{record['changed_at']}[/dim]")
    console.print()

    summary_raw = record.get("summary", [])
    summary: list[dict[str, object]] = summary_raw if isinstance(summary_raw, list) else []

    # Filter by category if specified
    if category:
        summary = [c for c in summary if str(c.get("category", "")).startswith(category)]

    if not summary:
        if category:
            print_warning(f"No changes found in category '{category}'.")
        else:
            print_warning("No changes in this record.")
        ctx.exit(0)

    # Group by change type
    added = [c for c in summary if c.get("type") == "added"]
    removed = [c for c in summary if c.get("type") == "removed"]
    modified = [c for c in summary if c.get("type") == "modified"]

    if added:
        console.print(f"[bold green]Added ({len(added)}):[/bold green]")
        for change in added:
            console.print(f"  [green]+[/green] {change['category']}: {change['entity']}")
        console.print()

    if removed:
        console.print(f"[bold red]Removed ({len(removed)}):[/bold red]")
        for change in removed:
            console.print(f"  [red]-[/red] {change['category']}: {change['entity']}")
        console.print()

    if modified:
        console.print(f"[bold yellow]Modified ({len(modified)}):[/bold yellow]")
        for change in modified:
            field = change.get("field", "")
            old = change.get("old", "")
            new = change.get("new", "")
            console.print(
                f"  [yellow]~[/yellow] {change['category']}: {change['entity']}"
                f".{field}: [red]{old}[/red] -> [green]{new}[/green]"
            )
        console.print()


@history.command("snapshot")
@click.argument("cluster")
@click.option(
    "--date",
    "-d",
    "target_date",
    required=True,
    help="Target date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.option(
    "--restore",
    is_flag=True,
    help="Restore this snapshot to the active cache.",
)
@click.pass_context
def snapshot_at_date(
    ctx: click.Context,
    cluster: str,
    target_date: str,
    output_json: bool,
    restore: bool,
) -> None:
    """Get the cache state for a cluster at a specific date.

    Returns the most recent snapshot recorded on or before the target date.
    This allows viewing what the cluster metadata looked like at any point in time.

    Examples:

        nf cache history snapshot cluster1 --date 2024-01-15
        nf cache history snapshot cluster1 -d 2024-06-01T12:00:00 --json
        nf cache history snapshot cluster1 -d 2024-01-15 --restore
    """
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-history")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    db = CacheHistoryDB(config=config)
    record = db.get_snapshot_at_date(cluster, target_date)
    db.close()

    if not record:
        print_error(f"No snapshot found for '{cluster}' on or before {target_date}.")
        ctx.exit(1)

    if output_json:
        after_json = record.get("after_json")
        output = {
            "id": record["id"],
            "cluster_name": record["cluster_name"],
            "snapshot_date": record["changed_at"],
            "requested_date": target_date,
            "metadata": json.loads(str(after_json)) if after_json else None,
        }
        console.print(json.dumps(output, indent=2, default=str))
        return

    if restore:
        # Restore to active cache
        from pynetappfoundry.cache import CachedClusterMetadata, ClusterMetadataDB

        after_json = record.get("after_json")
        if not after_json:
            print_error("Snapshot has no metadata to restore.")
            ctx.exit(1)

        try:
            snapshot_data = json.loads(str(after_json))
            snapshot_version = snapshot_data.get("cache_version")

            if not is_schema_compatible(snapshot_version):
                print_error(
                    f"Snapshot has incompatible schema version: {snapshot_version}. "
                    "Cannot restore to current cache format."
                )
                ctx.exit(1)

            metadata = CachedClusterMetadata.model_validate(snapshot_data)
            cache_db = ClusterMetadataDB(config=config)
            cache_db.set(cluster, metadata)
            cache_db.close()
            snapshot_date = str(record["changed_at"])[:10]
            console.print(
                f"[green]✓[/green] Restored cache for '{cluster}' "
                f"from snapshot #{record['id']} ({snapshot_date})"
            )
        except Exception as e:
            print_exception(f"Failed to restore snapshot: {e}", e)
            ctx.exit(1)
        return

    # Display summary
    console.print()
    console.print(f"[bold]Snapshot for {cluster}[/bold]")
    console.print(f"[cyan]Requested date:[/cyan] {target_date}")
    console.print(f"[cyan]Snapshot date:[/cyan]  {record['changed_at']}")
    console.print(f"[cyan]Record ID:[/cyan]      #{record['id']}")
    console.print()

    # Parse and show summary of the snapshot content
    after_json = record.get("after_json")
    if after_json:
        try:
            data = json.loads(str(after_json))
            _display_snapshot_summary(data)
        except json.JSONDecodeError:
            print_warning("Could not parse snapshot data.")
    console.print()
    console.print("[dim]Use --json to see full snapshot data[/dim]")
    console.print("[dim]Use --restore to restore this snapshot to the active cache[/dim]")
    console.print()


def _display_snapshot_summary(data: dict[str, object]) -> None:
    """Display a summary of snapshot contents.

    Args:
        data: Parsed snapshot data.
    """
    table = Table(title="Snapshot Contents")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right")

    # Extract nested dicts safely
    nodes = data.get("nodes", [])
    storage = data.get("storage", {})
    network = data.get("network", {})
    svms = data.get("svms", [])

    storage_dict = storage if isinstance(storage, dict) else {}
    network_dict = network if isinstance(network, dict) else {}

    # Count items in various categories
    categories: list[tuple[str, str | int]] = [
        ("Cluster Name", str(data.get("cluster_name", "N/A"))),
        ("Nodes", len(nodes) if isinstance(nodes, list) else 0),
        ("Aggregates", len(storage_dict.get("aggregates", []))),
        ("Volumes", len(storage_dict.get("volumes", []))),
        ("SVMs", len(svms) if isinstance(svms, list) else 0),
        ("Network Interfaces", len(network_dict.get("interfaces", []))),
        ("Network Ports", len(network_dict.get("ports", []))),
    ]

    for name, value in categories:
        table.add_row(name, str(value))

    console.print(table)


def _format_summary_brief(summary: list[dict[str, object]]) -> str:
    """Format a brief summary for table display.

    Args:
        summary: List of change dictionaries.

    Returns:
        Brief string summary.
    """
    if not summary:
        return "Initial capture"

    added = sum(1 for c in summary if c.get("type") == "added")
    removed = sum(1 for c in summary if c.get("type") == "removed")
    modified = sum(1 for c in summary if c.get("type") == "modified")

    parts = []
    if added:
        parts.append(f"+{added}")
    if removed:
        parts.append(f"-{removed}")
    if modified:
        parts.append(f"~{modified}")

    return " ".join(parts) if parts else "No changes"
