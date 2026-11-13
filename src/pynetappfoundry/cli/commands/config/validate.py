"""Config validation command."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

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


def _validate_clusters(config: Config, tree: Tree) -> list[str]:
    """Validate cluster configurations.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    clusters_branch = tree.add("[bold]Clusters[/bold]")

    clusters = config.data.get("clusters", {})
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


def _validate_users(config: Config, tree: Tree) -> list[str]:
    """Validate user credential configurations.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    users_branch = tree.add("[bold]Users[/bold]")

    users = config.settings.get("users", {})
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
                    errors.append(f"users.{utype}.{loc}: {err['msg']}")

    return errors


def _check_settings_section(
    config: Config,
    branch: Tree,
    *,
    label: str,
    keys: tuple[str, str],
    reader: Callable[[], object],
    absent_text: str,
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

    Returns:
        List of validation error messages.
    """
    top = config.settings.get(keys[0])
    if not isinstance(top, dict) or keys[1] not in top:
        branch.add(absent_text)
        return []
    try:
        reader()
    except ConfigurationError as e:
        branch.add(f"[red]{escape(label)}: Invalid[/red]")
        return [f"{'.'.join(keys)}: {e}"]
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


def _check_cluster_credentials(config: Config, tree: Tree) -> list[str]:
    """Check that all clusters have valid credentials.

    Args:
        config: Config instance to validate.
        tree: Rich Tree to add results to.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    creds_branch = tree.add("[bold]Cluster Credentials[/bold]")

    clusters = config.data.get("clusters", {})
    for name in clusters:
        try:
            user, _enc = config.get_user("clusters", name)
            creds_branch.add(f"[green]{escape(str(name))}: {escape(str(user))}[/green]")
        except ConfigurationError:
            creds_branch.add(f"[red]{escape(str(name))}: Missing credentials[/red]")
            errors.append(f"Cluster '{name}' has no credentials configured")

    return errors


@click.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """Validate configuration files.

    Checks that all configuration files are properly formatted and contain
    valid values. Reports any validation errors found.
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
    all_errors.extend(_validate_clusters(config, tree))
    all_errors.extend(_validate_users(config, tree))
    all_errors.extend(_validate_settings(config, tree))
    all_errors.extend(_check_cluster_credentials(config, tree))

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
