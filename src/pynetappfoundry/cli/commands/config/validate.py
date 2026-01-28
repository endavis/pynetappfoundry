"""Config validation command."""

from __future__ import annotations

from pathlib import Path

import click
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from pynetappfoundry.cli.utils import print_error, print_exception, print_success
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
            clusters_branch.add(f"[green]{name}[/green]")
        except ValidationError as e:
            clusters_branch.add(f"[red]{name}: Invalid[/red]")
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
                users_branch.add(f"[green]{utype}[/green]")
            except ValidationError as e:
                users_branch.add(f"[red]{utype}: Invalid[/red]")
                for err in e.errors():
                    loc = ".".join(str(x) for x in err["loc"])
                    errors.append(f"users.{utype}.{loc}: {err['msg']}")

    return errors


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

    # Validate ONTAP API settings
    try:
        config.get_ontap_api_settings()
        settings_branch.add("[green]ONTAP API[/green]")
    except ConfigurationError:
        settings_branch.add("[yellow]ONTAP API: Not configured[/yellow]")
    except ValidationError as e:
        settings_branch.add("[red]ONTAP API: Invalid[/red]")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            errors.append(f"ontapapi.general.{loc}: {err['msg']}")

    # Validate DII API settings (optional)
    try:
        config.get_dii_api_settings()
        settings_branch.add("[green]DII API[/green]")
    except ConfigurationError:
        settings_branch.add("[dim]DII API: Not configured (optional)[/dim]")
    except ValidationError as e:
        settings_branch.add("[red]DII API: Invalid[/red]")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            errors.append(f"diiapi.general.{loc}: {err['msg']}")

    # Validate SMTP settings (optional)
    try:
        config.get_smtp_settings()
        settings_branch.add("[green]SMTP[/green]")
    except ConfigurationError:
        settings_branch.add("[dim]SMTP: Not configured (optional)[/dim]")
    except ValidationError as e:
        settings_branch.add("[red]SMTP: Invalid[/red]")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            errors.append(f"settings.SMTP.{loc}: {err['msg']}")

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
            creds_branch.add(f"[green]{name}: {user}[/green]")
        except ConfigurationError:
            creds_branch.add(f"[red]{name}: Missing credentials[/red]")
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
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    console.print(f"\nValidating configuration in: [cyan]{config_path}[/cyan]\n")

    try:
        config = Config(config_dir=config_dir, script_name="config-validate")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

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
                "\n".join(f"[red]- {err}[/red]" for err in all_errors),
                title="[red]Validation Errors[/red]",
                border_style="red",
            )
        )
        print_error(f"\nValidation failed with {len(all_errors)} error(s)")
        ctx.exit(1)
    else:
        print_success("Configuration is valid")
