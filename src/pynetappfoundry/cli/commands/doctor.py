"""``nf doctor``: check configuration, environment and API access, with fix hints."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.options import filter_option, json_option
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.config_checks import (
    CheckResult,
    CheckSection,
    CheckStatus,
    run_static_checks,
)
from pynetappfoundry.doctor import API_NAMES

console = Console()

_STYLES = {
    CheckStatus.OK: "green",
    CheckStatus.ERROR: "red",
    CheckStatus.WARNING: "yellow",
    CheckStatus.SKIPPED: "dim",
}

# (group, section)
_Group = tuple[str, CheckSection]


def _parse_apis(value: str | None) -> tuple[str, ...]:
    """Parse ``--api``: comma-separated and case-insensitive; empty means every API."""
    if not value:
        return API_NAMES
    names = [part.strip().lower() for part in value.split(",") if part.strip()]
    unknown = [n for n in names if n not in API_NAMES]
    if unknown or not names:
        raise click.BadParameter(
            f"unknown API {', '.join(unknown) or value!r}; choose from {', '.join(API_NAMES)}",
            param_hint="--api",
        )
    return tuple(n for n in API_NAMES if n in names)


def _parse_filter(filter_str: str | None) -> dict[str, str]:
    """Parse ``--filter`` as ``with_config`` does."""
    if not filter_str:
        return {}
    try:
        parsed = json.loads(filter_str)
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid filter JSON: {e}") from e
    if not isinstance(parsed, dict):
        raise click.ClickException(
            f"Invalid filter JSON: expected a JSON object, got {type(parsed).__name__}"
        )
    return parsed


def _counts(groups: list[_Group]) -> dict[str, int]:
    """Count the results of every status."""
    counts = {status.value: 0 for status in CheckStatus}
    for _group, section in groups:
        for result in section.results:
            counts[result.status.value] += 1
    return counts


def _result_json(result: CheckResult) -> dict[str, Any]:
    return {
        "subject": result.subject,
        "status": result.status.value,
        "label": result.label,
        "errors": list(result.errors),
        "hint": result.hint,
    }


def _render(groups: list[_Group], tree: Tree) -> tuple[list[str], list[str]]:
    """Draw the results into ``tree``; return the error lines and hints of the errors."""
    errors: list[str] = []
    hints: list[str] = []
    for _group, section in groups:
        branch = tree.add(f"[bold]{escape(section.title)}[/bold]")
        for result in section.results:
            style = _STYLES[result.status]
            row = branch.add(f"[{style}]{escape(result.label)}[/{style}]")
            if result.hint and result.status is not CheckStatus.OK:
                hint_row = f"[yellow]{escape(result.hint)}[/yellow]"
                (branch if result.hint_as_sibling else row).add(hint_row)
            if result.status is CheckStatus.ERROR:
                errors.extend(result.errors)
                if result.hint:
                    hints.append(escape(result.hint))
    return errors, hints


@click.command()
@click.option(
    "--offline",
    is_flag=True,
    help="Skip the live checks: make no network request.",
)
@click.option(
    "--api",
    "api",
    type=str,
    help="Limit every check to these APIs, plus the shared sops and age-key checks: "
    "ontap, aiqum, dii, console, digitaladvisor (comma-separated).",
)
@click.option(
    "--scope",
    type=str,
    help="Check only this scope's settings, objects and accounts.",
)
@filter_option()
@json_option("Output results as JSON.")
@click.pass_context
def doctor(
    ctx: click.Context,
    offline: bool,
    api: str | None,
    scope: str | None,
    filter: str | None,  # click parameter name set by filter_option()
    output_json: bool,
) -> None:
    """Check configuration, environment and API access, with a fix hint per problem.

    Runs the static checks of 'nf config validate', then checks sops, the age
    key, every SOPS value and the caches, that config clusters match
    Console's by name, then sends one read-only request to
    each configured API. Warnings do not fail; any error exits 1.
    """
    apis = _parse_apis(api)
    selected = apis if api else None
    filter_dict = _parse_filter(filter)

    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        raise CliError(f"Configuration directory not found: {config_path}")
    try:
        config = Config(config_dir=config_dir, script_name="doctor")
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}", exc=e) from e
    if scope is not None:
        try:
            config.get_scope_settings(scope)
        except ConfigurationError as e:
            raise CliError(str(e)) from e

    try:
        clusters = {
            name: details
            for name, details in config.get_clusters(filter_dict).items()
            if scope is None or config.get_scope("clusters", name) == scope
        }
    except Exception as e:
        raise CliError(f"Failed to select clusters: {e}", exc=e) from e

    groups: list[_Group] = []
    from pynetappfoundry.doctor.selection import select_sections

    for section in select_sections(run_static_checks(config, scope), selected):
        groups.append(("static", CheckSection(f"Config: {section.title}", section.results)))

    from pynetappfoundry.doctor.environment import run_environment_checks

    groups.extend(
        ("environment", section)
        for section in run_environment_checks(
            config,
            scope=scope,
            apis=apis,
            sops_apis=selected,
            clusters=clusters,
            cluster_filter_active=bool(filter_dict),
        )
    )
    if not offline:
        from pynetappfoundry.doctor.live import run_live_checks

        groups.extend(
            ("live", section)
            for section in run_live_checks(config, apis=apis, scope=scope, clusters=clusters)
        )

    counts = _counts(groups)
    failed = counts[CheckStatus.ERROR.value]
    summary = ", ".join(f"{counts[s.value]} {s.value}" for s in CheckStatus)

    if output_json:
        document = {
            "sections": [
                {
                    "title": section.title,
                    "group": group,
                    "results": [_result_json(r) for r in section.results],
                }
                for group, section in groups
            ],
            "summary": counts,
            "offline": offline,
        }
        click.echo(json.dumps(document, indent=2))
        if failed:
            ctx.exit(1)
        return

    tree = Tree("[bold blue]nf doctor[/bold blue]")
    errors, hints = _render(groups, tree)
    console.print(tree)
    console.print()
    console.print(f"Summary: {summary}" + (" (offline)" if offline else ""))
    if errors:
        console.print(
            Panel(
                "\n".join(f"[red]- {escape(err)}[/red]" for err in errors),
                title="[red]Doctor Errors[/red]",
                border_style="red",
            )
        )
        raise CliError(f"Doctor found {failed} error(s)", hints=hints)
