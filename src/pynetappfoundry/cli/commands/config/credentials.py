"""Credential management commands."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from pynetappfoundry.cli.utils import print_error, print_success, print_warning
from pynetappfoundry.core.config import VALID_DATA_TYPES, Config
from pynetappfoundry.utils.sops import (
    SOPSError,
    SOPSNotInstalledError,
    encrypt_value,
    get_age_key_path,
    get_public_key_from_file,
    is_sops_installed,
)

console = Console()


def _encrypt_password(password: str, no_encrypt: bool, ctx: click.Context) -> str:
    """Encrypt password if SOPS is available.

    Args:
        password: Plain text password.
        no_encrypt: If True, skip encryption.
        ctx: Click context for exit.

    Returns:
        Encrypted password or original if no_encrypt.
    """
    if no_encrypt:
        return password

    if not is_sops_installed():
        print_warning("SOPS is not installed. Password will be stored as plain text.")
        print_warning("Run 'nf config init-sops' to set up encryption.")
        if not click.confirm("Continue with plain text storage?", default=False):
            ctx.exit(0)
        return password

    try:
        key_path = get_age_key_path()
        if not key_path.exists():
            print_error(f"Age key not found at {key_path}")
            console.print("Run 'nf config init-sops' to generate a keypair.")
            ctx.exit(1)

        public_key = get_public_key_from_file(key_path)
        console.print(f"Encrypting with key: {public_key[:20]}...")

        encrypted = encrypt_value(password, public_key)
        print_success("Password encrypted successfully.")
        return encrypted

    except SOPSNotInstalledError as e:
        print_error(str(e))
        ctx.exit(1)
        raise SystemExit(1) from None  # Unreachable but satisfies type checker
    except SOPSError as e:
        print_error(f"Encryption failed: {e}")
        ctx.exit(1)
        raise SystemExit(1) from None  # Unreachable but satisfies type checker


@click.command("set-credential")
@click.option(
    "--cluster",
    help="Name of the cluster to set credentials for (per-cluster override).",
)
@click.option(
    "--type",
    "cred_type",
    type=click.Choice(sorted(VALID_DATA_TYPES), case_sensitive=False),
    help="Set default credentials for all resources of this type (in users.toml).",
)
@click.option(
    "--user",
    required=True,
    help="Username.",
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password (will prompt if not provided).",
)
@click.option(
    "--no-encrypt",
    is_flag=True,
    help="Store password as plain text (not recommended).",
)
@click.pass_context
def set_credential(
    ctx: click.Context,
    cluster: str | None,
    cred_type: str | None,
    user: str,
    password: str,
    no_encrypt: bool,
) -> None:
    """Set encrypted credentials for a cluster or resource type.

    Use --cluster to set credentials for a specific cluster (stored in data file).
    Use --type to set default credentials for all resources of a type (stored in users.toml).

    Examples:

        # Set credentials for a specific cluster
        nf config set-credential --cluster mycluster --user admin

        # Set default credentials for all clusters
        nf config set-credential --type clusters --user admin
    """
    # Validate mutually exclusive options
    if cluster and cred_type:
        print_error("Cannot use both --cluster and --type. Choose one.")
        ctx.exit(1)

    if not cluster and not cred_type:
        print_error("Must specify either --cluster or --type.")
        console.print("\nExamples:")
        console.print("  nf config set-credential --cluster mycluster --user admin")
        console.print("  nf config set-credential --type clusters --user admin")
        ctx.exit(1)

    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir

    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="set-credential")
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        ctx.exit(1)

    # Encrypt password
    encrypted_password = _encrypt_password(password, no_encrypt, ctx)

    if cluster:
        _set_cluster_credential(ctx, config, config_path, cluster, user, encrypted_password)
    else:
        assert cred_type is not None  # For type checker
        _set_type_credential(ctx, config_path, cred_type, user, encrypted_password)


def _set_cluster_credential(
    ctx: click.Context,
    config: Config,
    config_path: Path,
    cluster: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Set credentials for a specific cluster."""
    # Check if cluster exists
    if cluster not in config.data.get("clusters", {}):
        print_error(f"Cluster '{cluster}' not found in configuration.")
        available = list(config.data.get("clusters", {}).keys())
        if available:
            console.print(f"Available clusters: {', '.join(available)}")
        ctx.exit(1)

    # Find and update the cluster's config file
    cluster_file = _find_cluster_file(config_path, cluster)
    if cluster_file is None:
        print_error(f"Could not find configuration file for cluster '{cluster}'")
        ctx.exit(1)

    try:
        _update_cluster_credentials(cluster_file, cluster, user, encrypted_password)
        print_success(f"Credentials updated for cluster '{cluster}'")
        console.print(f"  File: {cluster_file}")
        console.print(f"  User: {user}")
        _print_password_status(encrypted_password)
    except Exception as e:
        print_error(f"Failed to update configuration: {e}")
        ctx.exit(1)


def _set_type_credential(
    ctx: click.Context,
    config_path: Path,
    cred_type: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Set default credentials for a resource type in users.toml."""
    users_file = config_path / "users.toml"

    try:
        _update_users_credentials(users_file, cred_type, user, encrypted_password)
        print_success(f"Default credentials updated for type '{cred_type}'")
        console.print(f"  File: {users_file}")
        console.print(f"  User: {user}")
        _print_password_status(encrypted_password)
    except Exception as e:
        print_error(f"Failed to update configuration: {e}")
        ctx.exit(1)


def _print_password_status(encrypted_password: str) -> None:
    """Print password encryption status."""
    if encrypted_password.startswith("SOPS["):
        console.print("  Password: [dim](encrypted)[/dim]")
    else:
        console.print("  Password: [yellow](plain text)[/yellow]")


def _find_cluster_file(config_path: Path, cluster_name: str) -> Path | None:
    """Find the configuration file containing a cluster.

    Args:
        config_path: Path to the configuration directory.
        cluster_name: Name of the cluster to find.

    Returns:
        Path to the file, or None if not found.
    """
    import tomllib

    # Check data/clusters directory first
    clusters_dir = config_path / "data" / "clusters"
    if clusters_dir.exists():
        for toml_file in clusters_dir.glob("*.toml"):
            try:
                with open(toml_file, "rb") as f:
                    data = tomllib.load(f)
                if cluster_name in data.get("clusters", {}):
                    return toml_file
            except Exception:  # nosec B112
                continue

    # Check main data directory
    data_dir = config_path / "data"
    if data_dir.exists():
        for toml_file in data_dir.glob("*.toml"):
            try:
                with open(toml_file, "rb") as f:
                    data = tomllib.load(f)
                if cluster_name in data.get("clusters", {}):
                    return toml_file
            except Exception:  # nosec B112
                continue

    return None


def _update_cluster_credentials(
    file_path: Path,
    cluster_name: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Update cluster credentials in a TOML file.

    Args:
        file_path: Path to the TOML file.
        cluster_name: Name of the cluster.
        user: Username to set.
        encrypted_password: Encrypted or plain password.
    """
    import tomllib

    import tomli_w

    # Read current content
    with open(file_path, "rb") as f:
        data = tomllib.load(f)

    # Update credentials
    if "clusters" not in data:
        data["clusters"] = {}
    if cluster_name not in data["clusters"]:
        data["clusters"][cluster_name] = {}

    data["clusters"][cluster_name]["user"] = user
    data["clusters"][cluster_name]["enc"] = encrypted_password

    # Write back
    with open(file_path, "wb") as f:
        tomli_w.dump(data, f)


def _update_users_credentials(
    users_file: Path,
    cred_type: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Update default credentials in users.toml.

    Args:
        users_file: Path to users.toml.
        cred_type: Resource type (e.g., 'clusters').
        user: Username to set.
        encrypted_password: Encrypted or plain password.
    """
    import tomllib

    import tomli_w

    # Read current content or start fresh
    if users_file.exists():
        with open(users_file, "rb") as f:
            data = tomllib.load(f)
    else:
        data = {}

    # Update credentials for the type
    if cred_type not in data:
        data[cred_type] = {}

    data[cred_type]["user"] = user
    data[cred_type]["enc"] = encrypted_password

    # Write back
    with open(users_file, "wb") as f:
        tomli_w.dump(data, f)
