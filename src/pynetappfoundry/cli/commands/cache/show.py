"""Cache show command."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cache.db import all_realtime_attrs
from pynetappfoundry.cli.utils import (
    format_value_markup,
    print_error,
    print_exception,
    print_warning,
)
from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)
console = Console()


def _strip_realtime_fields(data: dict[str, object], rt_attrs: frozenset[str]) -> dict[str, object]:
    """Remove realtime fields from a nested model dump dict.

    Args:
        data: Dictionary from ``model_dump()``.
        rt_attrs: Set of realtime attribute names to strip.

    Returns:
        New dictionary with realtime keys removed at every nesting level.
    """
    result: dict[str, object] = {}
    for key, value in data.items():
        if key in rt_attrs:
            continue
        if isinstance(value, dict):
            result[key] = _strip_realtime_fields(value, rt_attrs)
        elif isinstance(value, list):
            result[key] = [
                _strip_realtime_fields(item, rt_attrs) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def _format_value(value: object) -> str:
    """Format a value for display.

    Args:
        value: Value to format.

    Returns:
        Formatted string.
    """
    result = format_value_markup(value)
    if result is not None:
        return result
    if isinstance(value, list):
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
        print_exception(f"Failed to load configuration: {e}", e)
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
    try:
        metadata = db.get(cluster)
    except ValueError as e:
        logger.debug("Invalid cluster name: %s", e)
        db.close()
        print_error(f"Invalid cluster name: '{cluster}'")
        # Check if it looks like a query path
        if "." in cluster or "[" in cluster:
            console.print("Did you mean to use [cyan]nf cache query[/cyan] instead?")
            console.print(f"  Example: nf cache query --all {cluster}")
        ctx.exit(1)
    db.close()

    if not metadata:
        print_error(f"No cached data found for cluster '{cluster}'.")
        console.print("Use 'nf cache refresh {cluster}' to populate the cache.")
        ctx.exit(1)

    rt = all_realtime_attrs()

    if output_json:
        data = _strip_realtime_fields(metadata.model_dump(mode="json"), rt)
        console.print_json(json.dumps(data, indent=2))
        return

    # Build display tree
    data = _strip_realtime_fields(metadata.model_dump(), rt)

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
