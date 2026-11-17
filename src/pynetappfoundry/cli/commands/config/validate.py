"""Config validation command."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import click
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.utils import print_success
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.models import (
    ClusterConfig,
    UserCredentials,
)

console = Console()


def _clusters_in_scope(config: Config, scope: str | None) -> dict[str, Any]:
    """Return the clusters to check: all of them, or only those of ``scope``."""
    clusters: dict[str, Any] = config.data.get("clusters", {})
    if scope is None:
        return clusters
    return {
        name: data for name, data in clusters.items() if config.get_scope("clusters", name) == scope
    }


def _validate_clusters(config: Config, tree: Tree, scope: str | None = None) -> list[str]:
    """Validate cluster configurations.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.
        scope: Check only this scope's clusters; None checks every cluster.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    clusters_branch = tree.add("[bold]Clusters[/bold]")

    clusters = _clusters_in_scope(config, scope)
    if not clusters:
        clusters_branch.add("[yellow]No clusters configured[/yellow]")
        return errors

    for name, cluster_data in clusters.items():
        try:
            ClusterConfig.model_validate(cluster_data)
            clusters_branch.add(f"[green]{escape(str(name))}[/green]")
        except ValidationError as e:
            clusters_branch.add(f"[red]{escape(str(name))}: Invalid[/red]")
            for err in e.errors():
                loc = ".".join(str(x) for x in err["loc"])
                errors.append(f"clusters.{name}.{loc}: {err['msg']}")

    return errors


def _validate_users(users: dict[str, Any], tree: Tree, *, label_prefix: str = "users") -> list[str]:
    """Validate user credential configurations.

    Args:
        users: The parsed ``users.toml`` sections to validate.
        tree: Rich Tree to add results to.
        label_prefix: Prefix of each error key, ``users`` or ``<scope>/users``.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    users_branch = tree.add("[bold]Users[/bold]")

    if not users:
        users_branch.add("[yellow]No users configured[/yellow]")
        return errors

    for utype, udata in users.items():
        if isinstance(udata, dict) and "user" in udata:
            try:
                UserCredentials.model_validate(udata)
                users_branch.add(f"[green]{escape(str(utype))}[/green]")
            except ValidationError as e:
                users_branch.add(f"[red]{escape(str(utype))}: Invalid[/red]")
                for err in e.errors():
                    loc = ".".join(str(x) for x in err["loc"])
                    errors.append(f"{label_prefix}.{utype}.{loc}: {err['msg']}")

    return errors


def _check_settings_section(
    config: Config,
    branch: Tree,
    *,
    label: str,
    keys: tuple[str, str],
    reader: Callable[[], object],
    absent_text: str,
    tree: dict[str, Any] | None = None,
    error_prefix: str = "",
) -> list[str]:
    """Report one settings section as valid, not configured, or invalid.

    A section that is absent is "not configured". A section that is present but
    fails to load (invalid fields, a SOPS value that cannot be decrypted) is
    invalid, and the reader's error message is returned as a validation error.

    Args:
        config: Config instance to validate.
        branch: Rich tree branch to add the result to.
        label: Display name of the section.
        keys: ``(top-level key, section key)`` locating the section in ``config.settings``.
        reader: The ``Config`` reader that loads and validates the section.
        absent_text: Markup shown when the section is absent.
        tree: Settings to look in instead of ``config.settings`` (a scope's own tree).
        error_prefix: Prefix of the error key, such as ``Org1/`` for a scope.

    Returns:
        List of validation error messages.
    """
    top = (config.settings if tree is None else tree).get(keys[0])
    if not isinstance(top, dict) or keys[1] not in top:
        branch.add(absent_text)
        return []
    try:
        reader()
    except ConfigurationError as e:
        branch.add(f"[red]{escape(label)}: Invalid[/red]")
        return [f"{error_prefix}{'.'.join(keys)}: {e}"]
    branch.add(f"[green]{escape(label)}[/green]")
    return []


def _validate_settings(config: Config, tree: Tree) -> list[str]:
    """Validate settings configurations.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    settings_branch = tree.add("[bold]Settings[/bold]")

    errors.extend(
        _check_settings_section(
            config,
            settings_branch,
            label="ONTAP API",
            keys=("ontapapi", "general"),
            reader=config.get_ontap_api_settings,
            absent_text="[yellow]ONTAP API: Not configured[/yellow]",
        )
    )
    errors.extend(
        _check_settings_section(
            config,
            settings_branch,
            label="DII API",
            keys=("diiapi", "general"),
            reader=config.get_dii_api_settings,
            absent_text="[dim]DII API: Not configured (optional)[/dim]",
        )
    )
    errors.extend(
        _check_settings_section(
            config,
            settings_branch,
            label="SMTP",
            keys=("settings", "SMTP"),
            reader=config.get_smtp_settings,
            absent_text="[dim]SMTP: Not configured (optional)[/dim]",
        )
    )

    # Validate licensing settings (optional)
    licensing = config.get_licensing_settings()
    if licensing:
        settings_branch.add("[green]Licensing[/green]")
    else:
        settings_branch.add("[dim]Licensing: Not configured (optional)[/dim]")

    return errors


def _validate_scope_settings(config: Config, tree: Tree, scope: str) -> list[str]:
    """Validate a scope's ``monitoring.toml`` and Console account.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.
        scope: A known scope name.

    Returns:
        List of validation error messages.
    """
    scope_tree = config.get_scope_settings(scope)
    branch = tree.add(f"[bold]Scope settings ({escape(scope)})[/bold]")
    if scope_tree.get("monitoring"):
        branch.add("[green]Monitoring[/green]")
    else:
        branch.add("[dim]Monitoring: Not configured (optional)[/dim]")
    return _check_settings_section(
        config,
        branch,
        label="Console",
        keys=("consoleapi", "general"),
        reader=lambda: config.get_console_api_settings(scope=scope),
        absent_text="[dim]Console: Not configured (optional)[/dim]",
        tree=scope_tree,
        error_prefix=f"{scope}/",
    )


def _check_cluster_credentials(config: Config, tree: Tree, scope: str | None = None) -> list[str]:
    """Check that all clusters have valid credentials.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.
        scope: Check only this scope's clusters; None checks every cluster.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    creds_branch = tree.add("[bold]Cluster Credentials[/bold]")

    clusters = _clusters_in_scope(config, scope)
    for name in clusters:
        try:
            user, _enc = config.get_user("clusters", name)
            creds_branch.add(f"[green]{escape(str(name))}: {escape(str(user))}[/green]")
        except ConfigurationError:
            creds_branch.add(f"[red]{escape(str(name))}: Missing credentials[/red]")
            errors.append(f"Cluster '{name}' has no credentials configured")

    return errors


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

    # Build validation tree
    tree = Tree("[bold blue]Configuration Validation[/bold blue]")
    all_errors: list[str] = []

    # Validate each section
    if scope is None:
        all_errors.extend(_validate_clusters(config, tree))
        all_errors.extend(_validate_users(config.settings.get("users", {}), tree))
        all_errors.extend(_validate_settings(config, tree))
        all_errors.extend(_check_cluster_credentials(config, tree))
    else:
        try:
            scope_tree = config.get_scope_settings(scope)
        except ConfigurationError as e:
            raise CliError(str(e)) from e
        all_errors.extend(_validate_clusters(config, tree, scope))
        all_errors.extend(
            _validate_users(scope_tree.get("users", {}), tree, label_prefix=f"{scope}/users")
        )
        all_errors.extend(_validate_scope_settings(config, tree, scope))
        all_errors.extend(_check_cluster_credentials(config, tree, scope))

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
        raise CliError(f"\nValidation failed with {len(all_errors)} error(s)")
    else:
        print_success("Configuration is valid")
