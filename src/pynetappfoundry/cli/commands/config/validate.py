"""Config validation command."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.utils import print_success
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.config_checks import CheckSection, CheckStatus, run_static_checks

console = Console()


_STYLES = {
    CheckStatus.OK: "green",
    CheckStatus.ERROR: "red",
    CheckStatus.WARNING: "yellow",
    CheckStatus.SKIPPED: "dim",
}


def _render(sections: list[CheckSection], tree: Tree) -> tuple[list[str], list[str]]:
    """Draw the check results into ``tree``.

    Args:
        sections: Results from :func:`run_static_checks`.
        tree: Rich Tree to add the sections to.

    Returns:
        ``(errors, hints)``: the error-panel lines and the hints of the ``error``
        results, already escaped for printing.
    """
    errors: list[str] = []
    hints: list[str] = []
    for section in sections:
        branch = tree.add(f"[bold]{escape(section.title)}[/bold]")
        for result in section.results:
            style = _STYLES[result.status]
            row = branch.add(f"[{style}]{escape(result.label)}[/{style}]")
            if result.hint:
                hint_row = f"[yellow]{escape(result.hint)}[/yellow]"
                (branch if result.hint_as_sibling else row).add(hint_row)
            if result.status is CheckStatus.ERROR:
                errors.extend(result.errors)
                if result.hint:
                    hints.append(escape(result.hint))
    return errors, hints


@click.command()
@click.option(
    "--scope",
    type=str,
    help=(
        "Also check this scope: its clusters, users.toml, monitoring.toml and "
        "Console account. Without it, validation is unchanged."
    ),
)
@click.pass_context
def validate(ctx: click.Context, scope: str | None) -> None:
    """Validate configuration files.

    Checks that all configuration files are properly formatted and contain
    valid values. Reports any validation errors found. With --scope, checks
    that one scope's own files instead of the root settings.
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        raise CliError(f"Configuration directory not found: {config_path}")

    console.print(f"\nValidating configuration in: [cyan]{escape(str(config_path))}[/cyan]\n")

    try:
        config = Config(config_dir=config_dir, script_name="config-validate")
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}", exc=e) from e

    if scope is not None:
        try:
            config.get_scope_settings(scope)
        except ConfigurationError as e:
            raise CliError(str(e)) from e

    tree = Tree("[bold blue]Configuration Validation[/bold blue]")
    all_errors, advice = _render(run_static_checks(config, scope), tree)

    # Print the tree
    console.print(tree)
    console.print()

    # Summary
    if all_errors:
        console.print(
            Panel(
                "\n".join(f"[red]- {escape(err)}[/red]" for err in all_errors),
                title="[red]Validation Errors[/red]",
                border_style="red",
            )
        )
        raise CliError(f"\nValidation failed with {len(all_errors)} error(s)", hints=advice)
    else:
        print_success("Configuration is valid")
