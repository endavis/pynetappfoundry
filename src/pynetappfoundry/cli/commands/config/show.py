"""Config show command."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cli.utils import print_error
from pynetappfoundry.core.config import Config

console = Console()

# Pattern for detecting sensitive keys
SENSITIVE_KEYS = {"password", "enc", "token", "secret", "key", "api_key", "api_token"}


def _mask_sensitive(data: Any, unmask: bool = False) -> Any:
    """Recursively mask sensitive values in data.

    Args:
        data: Data to process.
        unmask: If True, don't mask values.

    Returns:
        Data with sensitive values masked.
    """
    if unmask:
        return data

    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
                if isinstance(value, str) and value:
                    result[key] = "********"
                else:
                    result[key] = value
            else:
                result[key] = _mask_sensitive(value, unmask)
        return result
    elif isinstance(data, list):
        return [_mask_sensitive(item, unmask) for item in data]
    else:
        return data


def _format_value(value: Any, indent: int = 0) -> str:
    """Format a value for display.

    Args:
        value: Value to format.
        indent: Current indentation level.

    Returns:
        Formatted string.
    """
    prefix = "  " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for k, v in value.items():
            formatted_v = _format_value(v, indent + 1)
            if isinstance(v, dict) and v:
                lines.append(f"{prefix}  [cyan]{k}[/cyan]:")
                lines.append(formatted_v)
            else:
                lines.append(f"{prefix}  [cyan]{k}[/cyan]: {formatted_v}")
        return "\n".join(lines)
    elif isinstance(value, list):
        if not value:
            return "[]"
        return "[" + ", ".join(str(v) for v in value) + "]"
    elif isinstance(value, str):
        if value == "********":
            return "[dim]********[/dim]"
        return f"[green]{value}[/green]"
    elif isinstance(value, bool):
        return f"[yellow]{value}[/yellow]"
    elif isinstance(value, (int, float)):
        return f"[magenta]{value}[/magenta]"
    else:
        return str(value)


def _build_tree(tree: Tree, data: dict[str, Any], unmask: bool = False) -> None:
    """Build a Rich tree from configuration data.

    Args:
        tree: Rich Tree to populate.
        data: Configuration data.
        unmask: If True, don't mask sensitive values.
    """
    masked_data = _mask_sensitive(data, unmask)

    for key, value in masked_data.items():
        if isinstance(value, dict) and value:
            branch = tree.add(f"[bold cyan]{key}[/bold cyan]")
            _build_tree(branch, value, unmask=True)  # Already masked at top level
        else:
            formatted = _format_value(value)
            tree.add(f"[cyan]{key}[/cyan]: {formatted}")


@click.command()
@click.option(
    "--section",
    "-s",
    type=str,
    help="Show only a specific section (e.g., 'clusters', 'settings', 'users').",
)
@click.option(
    "--unmask",
    is_flag=True,
    default=False,
    help="Show passwords and tokens unmasked (use with caution).",
)
@click.pass_context
def show(ctx: click.Context, section: str | None, unmask: bool) -> None:
    """Display current configuration.

    Shows the loaded configuration with sensitive values masked by default.
    Use --unmask to reveal passwords and tokens (use with caution).

    Examples:

        nf config show                    # Show all config
        nf config show -s clusters        # Show only clusters
        nf config show -s settings        # Show only settings
        nf config show --unmask           # Show with passwords visible
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="config-show")
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        ctx.exit(1)

    console.print(f"\nConfiguration from: [cyan]{config_path}[/cyan]\n")

    if unmask:
        console.print("[yellow]Warning: Sensitive values are unmasked![/yellow]\n")

    # Determine what to show
    if section:
        section_lower = section.lower()
        # Check in data first (clusters, aiqums, etc.)
        if section_lower in config.data:
            tree = Tree(f"[bold blue]{section}[/bold blue]")
            _build_tree(tree, config.data[section_lower], unmask)
            console.print(tree)
        # Check in settings
        elif section_lower in config.settings:
            tree = Tree(f"[bold blue]{section}[/bold blue]")
            _build_tree(tree, config.settings[section_lower], unmask)
            console.print(tree)
        else:
            available = list(config.data.keys()) + list(config.settings.keys())
            print_error(f"Section '{section}' not found.")
            console.print(f"Available sections: {', '.join(available)}")
            ctx.exit(1)
    else:
        # Show everything
        # Data sections
        if config.data:
            data_tree = Tree("[bold blue]Data[/bold blue]")
            for data_type, items in config.data.items():
                if items:
                    type_branch = data_tree.add(f"[bold]{data_type}[/bold] ({len(items)} items)")
                    for name, item_data in items.items():
                        item_branch = type_branch.add(f"[cyan]{name}[/cyan]")
                        masked = _mask_sensitive(item_data, unmask)
                        for k, v in masked.items():
                            if k != "name":  # Skip redundant name
                                formatted = _format_value(v)
                                item_branch.add(f"{k}: {formatted}")
            console.print(data_tree)
            console.print()

        # Settings sections
        if config.settings:
            settings_tree = Tree("[bold blue]Settings[/bold blue]")
            _build_tree(settings_tree, config.settings, unmask)
            console.print(settings_tree)

    # Show summary
    console.print()
    summary_lines = [
        f"Config directory: {config.config_dir}",
        f"Clusters: {len(config.data.get('clusters', {}))}",
        f"Settings files: {len(config.settings)}",
    ]
    console.print(Panel("\n".join(summary_lines), title="Summary", border_style="dim"))
