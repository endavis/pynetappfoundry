"""Credential management commands."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from pynetappfoundry.cli.utils import print_error, print_success, print_warning
from pynetappfoundry.core.config import Config
from pynetappfoundry.utils.sops import (
    SOPSError,
    SOPSNotInstalledError,
    encrypt_value,
    get_age_key_path,
    get_public_key_from_file,
    is_sops_installed,
)

console = Console()


@click.command("set-credential")
@click.option(
    "--cluster",
    required=True,
    help="Name of the cluster to set credentials for.",
)
@click.option(
    "--user",
    required=True,
    help="Username for the cluster.",
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password for the cluster (will prompt if not provided).",
)
@click.option(
    "--no-encrypt",
    is_flag=True,
    help="Store password as plain text (not recommended).",
)
@click.pass_context
def set_credential(
    ctx: click.Context,
    cluster: str,
    user: str,
    password: str,
    no_encrypt: bool,
) -> None:
    """Set encrypted credentials for a cluster.

    This command encrypts the password using SOPS/age and stores it
    in the cluster's configuration file.

    Example:

        nf config set-credential --cluster mycluster --user admin

        # Will prompt for password securely
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="set-credential")
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        ctx.exit(1)

    # Check if cluster exists
    if cluster not in config.data.get("clusters", {}):
        print_error(f"Cluster '{cluster}' not found in configuration.")
        available = list(config.data.get("clusters", {}).keys())
        if available:
            console.print(f"Available clusters: {', '.join(available)}")
        ctx.exit(1)

    # Encrypt password if SOPS is available
    encrypted_password = password
    if not no_encrypt:
        if not is_sops_installed():
            print_warning("SOPS is not installed. Password will be stored as plain text.")
            print_warning("Run 'nf config init-sops' to set up encryption.")
            if not click.confirm("Continue with plain text storage?", default=False):
                ctx.exit(0)
        else:
            try:
                # Get public key for encryption
                key_path = get_age_key_path()
                if not key_path.exists():
                    print_error(f"Age key not found at {key_path}")
                    console.print("Run 'nf config init-sops' to generate a keypair.")
                    ctx.exit(1)

                public_key = get_public_key_from_file(key_path)
                console.print(f"Encrypting with key: {public_key[:20]}...")

                encrypted_password = encrypt_value(password, public_key)
                print_success("Password encrypted successfully.")

            except SOPSNotInstalledError as e:
                print_error(str(e))
                ctx.exit(1)
            except SOPSError as e:
                print_error(f"Encryption failed: {e}")
                ctx.exit(1)

    # Find and update the cluster's config file
    cluster_file = _find_cluster_file(config_path, cluster)
    if cluster_file is None:
        print_error(f"Could not find configuration file for cluster '{cluster}'")
        ctx.exit(1)

    # Update the file
    try:
        _update_cluster_credentials(cluster_file, cluster, user, encrypted_password)
        print_success(f"Credentials updated for cluster '{cluster}'")
        console.print(f"  File: {cluster_file}")
        console.print(f"  User: {user}")
        if encrypted_password != password:
            console.print("  Password: [dim](encrypted)[/dim]")
        else:
            console.print("  Password: [yellow](plain text)[/yellow]")
    except Exception as e:
        print_error(f"Failed to update configuration: {e}")
        ctx.exit(1)


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
