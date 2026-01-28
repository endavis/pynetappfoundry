"""Cache show command."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cli.utils import print_error, print_warning
from pynetappfoundry.core.config import Config

console = Console()


def _format_value(value: object) -> str:
    """Format a value for display.

    Args:
        value: Value to format.

    Returns:
        Formatted string.
    """
    if isinstance(value, bool):
        return f"[yellow]{value}[/yellow]"
    elif isinstance(value, (int, float)):
        return f"[magenta]{value}[/magenta]"
    elif isinstance(value, str):
        if not value:
            return "[dim](empty)[/dim]"
        return f"[green]{value}[/green]"
    elif isinstance(value, list):
        if not value:
            return "[dim](empty list)[/dim]"
        return f"[cyan]{len(value)} items[/cyan]"
    return str(value)


def _build_tree_from_dict(
    tree: Tree, data: dict[str, object], max_depth: int = 3, depth: int = 0
) -> None:
    """Build a Rich tree from a dictionary.

    Args:
        tree: Rich Tree to populate.
        data: Dictionary data.
        max_depth: Maximum nesting depth to display.
        depth: Current depth.
    """
    for key, value in data.items():
        if key.startswith("_"):
            continue  # Skip internal keys

        if isinstance(value, dict) and depth < max_depth:
            branch = tree.add(f"[bold cyan]{key}[/bold cyan]")
            _build_tree_from_dict(branch, value, max_depth, depth + 1)
        elif isinstance(value, list) and depth < max_depth:
            if value and isinstance(value[0], dict):
                branch = tree.add(f"[bold cyan]{key}[/bold cyan] ({len(value)} items)")
                for i, item in enumerate(value[:5]):  # Show first 5
                    item_branch = branch.add(f"[dim]#{i + 1}[/dim]")
                    _build_tree_from_dict(item_branch, item, max_depth, depth + 1)
                if len(value) > 5:
                    branch.add(f"[dim]... and {len(value) - 5} more[/dim]")
            else:
                tree.add(f"[cyan]{key}[/cyan]: {_format_value(value)}")
        else:
            tree.add(f"[cyan]{key}[/cyan]: {_format_value(value)}")


@click.command()
@click.argument("cluster", required=False)
@click.option(
    "--section",
    "-s",
    type=click.Choice(
        ["cloud", "cluster", "nodes", "network", "storage", "licenses", "ha", "relationships"],
        case_sensitive=False,
    ),
    help="Show only a specific section.",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.pass_context
def show(ctx: click.Context, cluster: str | None, section: str | None, output_json: bool) -> None:
    """Display cached metadata for a cluster.

    If CLUSTER is not specified, lists all cached clusters.

    Examples:

        nf cache show                    # List cached clusters
        nf cache show cluster1           # Show all cached data
        nf cache show cluster1 -s nodes  # Show only nodes
        nf cache show cluster1 --json    # Output as JSON
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-show")
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        ctx.exit(1)

    db = ClusterMetadataDB(config=config)

    if not cluster:
        # List all cached clusters
        clusters = db.list_clusters()
        if not clusters:
            print_warning("No cached clusters found. Use 'nf cache refresh' to populate.")
            ctx.exit(0)

        console.print("\n[bold]Cached Clusters:[/bold]\n")
        for c in clusters:
            console.print(
                f"  [cyan]{c['cluster_name']}[/cyan] - "
                f"cached at {c['cached_at']} (version {c['cache_version']})"
            )
        console.print()
        db.close()
        return

    # Show specific cluster
    metadata = db.get(cluster)
    db.close()

    if not metadata:
        print_error(f"No cached data found for cluster '{cluster}'.")
        console.print("Use 'nf cache refresh {cluster}' to populate the cache.")
        ctx.exit(1)

    if output_json:
        console.print(metadata.model_dump_json(indent=2))
        return

    # Build display tree
    data = metadata.model_dump()

    if section:
        section_lower = section.lower()
        if section_lower not in data:
            print_error(f"Section '{section}' not found.")
            ctx.exit(1)
        section_data = data[section_lower]
        tree = Tree(f"[bold blue]{cluster} - {section}[/bold blue]")
        if isinstance(section_data, dict):
            _build_tree_from_dict(tree, section_data)
        elif isinstance(section_data, list):
            for i, item in enumerate(section_data):
                if isinstance(item, dict):
                    item_branch = tree.add(f"[dim]#{i + 1}[/dim]")
                    _build_tree_from_dict(item_branch, item)
                else:
                    tree.add(str(item))
    else:
        tree = Tree(f"[bold blue]{cluster}[/bold blue]")
        _build_tree_from_dict(tree, data)

    console.print()
    console.print(tree)

    # Summary panel
    summary = [
        f"Cluster: {metadata.cluster_name}",
        f"Cached at: {metadata.cached_at.isoformat()}",
        f"Cache version: {metadata.cache_version}",
        f"Stale: {'Yes' if metadata.is_stale() else 'No'}",
    ]
    console.print()
    console.print(Panel("\n".join(summary), title="Cache Info", border_style="dim"))
