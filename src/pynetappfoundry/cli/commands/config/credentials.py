"""Credential management commands."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape

from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.utils import print_success, print_warning
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


def _load_public_key() -> str:
    """Read the age public key from the configured key file.

    Returns:
        The age public key.

    Raises:
        CliError: If the age key file does not exist.
    """
    key_path = get_age_key_path()
    if not key_path.exists():
        raise CliError(
            f"Age key not found at {key_path}",
            hints=["Run 'nf config init-sops' to generate a keypair."],
        )
    return get_public_key_from_file(key_path)


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
        public_key = _load_public_key()
        console.print(f"Encrypting with key: {escape(public_key[:20])}...")

        encrypted = encrypt_value(password, public_key)
        print_success("Password encrypted successfully.")
        return encrypted

    except SOPSNotInstalledError as e:
        raise CliError(str(e)) from e
    except SOPSError as e:
        raise CliError(f"Encryption failed: {e}") from e


@click.command("encrypt-value")
@click.option(
    "--value",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Value to encrypt (will prompt, hidden, if not provided).",
)
def encrypt_value_cmd(value: str) -> None:
    """Encrypt a value into a SOPS[...] string for a settings file.

    Prints only the SOPS[...] value to stdout (status messages go to stderr), so the
    output pipes cleanly. Paste it into settings.toml [SMTP] password, diiapi.toml
    api_ro_token, or consoleapi.toml client_secret, service_token or user_token.

    Examples:

        nf config encrypt-value

        nf config encrypt-value > value.txt
    """
    if not is_sops_installed():
        raise CliError(
            "SOPS is not installed; cannot encrypt the value.",
            hints=["Install sops, then run 'nf config init-sops' to set up encryption."],
        )

    try:
        public_key = _load_public_key()
        encrypted = encrypt_value(value, public_key)
    except SOPSNotInstalledError as e:
        raise CliError(str(e)) from e
    except SOPSError as e:
        raise CliError(f"Encryption failed: {e}") from e

    click.echo("Value encrypted successfully.", err=True)
    click.echo(encrypted)


@click.command("set-credential")
@click.option(
    "--cluster",
    help="Name of the cluster to set credentials for. Alias for '--type clusters --name NAME'.",
)
@click.option(
    "--type",
    "cred_type",
    type=click.Choice(sorted(VALID_DATA_TYPES | {"console"}), case_sensitive=False),
    help=(
        "Set default credentials for all resources of this type (in users.toml), "
        "or with --name for one object. "
        "'console' stores the Console refresh token: --user is only a label and "
        "the password prompt takes the refresh token."
    ),
)
@click.option(
    "--name",
    "obj_name",
    help=(
        "Name of one inventory object of --type (for example an AIQUM or a Cloud "
        "Insights tenant). Its credentials are stored on its data file entry. "
        "For a token-style secret, --user is only a label and the password prompt "
        "takes the token."
    ),
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
    obj_name: str | None,
    user: str,
    password: str,
    no_encrypt: bool,
) -> None:
    """Set encrypted credentials for an inventory object or resource type.

    Use --type with --name to set credentials for one object of any inventory
    type (stored on its data file entry); --cluster NAME is an alias for
    --type clusters --name NAME.
    Use --type alone to set default credentials for all resources of a type
    (stored in users.toml).

    Examples:

        # Set credentials for a specific cluster
        nf config set-credential --cluster mycluster --user admin

        # Same, with --type and --name
        nf config set-credential --type clusters --name mycluster --user admin

        # Set credentials for one AIQUM
        nf config set-credential --type aiqums --name aiqum1 --user admin

        # Store a Cloud Insights tenant API token (the user is a label; the
        # password prompt takes the token)
        nf config set-credential --type cloudinsights --name tenant1 --user token

        # Set default credentials for all clusters
        nf config set-credential --type clusters --user admin

        # Store the Console refresh token (the user is a label, never sent;
        # the password prompt takes the refresh token)
        nf config set-credential --type console --user console
    """
    # Validate mutually exclusive options
    if cluster and cred_type:
        raise CliError("Cannot use both --cluster and --type. Choose one.")

    if cluster and obj_name:
        raise CliError("Cannot use both --cluster and --name. Choose one.")

    if not cluster and not cred_type:
        if obj_name:
            raise CliError("--name requires --type.")
        raise CliError(
            "Must specify either --cluster or --type.",
            hints=[
                "\nExamples:",
                "  nf config set-credential --cluster mycluster --user admin",
                "  nf config set-credential --type clusters --user admin",
                "  nf config set-credential --type aiqums --name aiqum1 --user admin",
            ],
        )

    if cred_type == "console" and obj_name:
        raise CliError(
            "--type console takes no --name; the Console refresh token is org-wide.",
            hints=["Run 'nf config set-credential --type console --user <label>'."],
        )

    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir

    if not config_path.exists():
        raise CliError(f"Configuration directory not found: {config_path}")

    try:
        config = Config(config_dir=config_dir, script_name="set-credential")
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}") from e

    # Encrypt password
    encrypted_password = _encrypt_password(password, no_encrypt, ctx)

    if cluster:
        _set_object_credential(config, config_path, "clusters", cluster, user, encrypted_password)
    elif obj_name:
        assert cred_type is not None  # For type checker
        _set_object_credential(config, config_path, cred_type, obj_name, user, encrypted_password)
    else:
        assert cred_type is not None  # For type checker
        _set_type_credential(ctx, config_path, cred_type, user, encrypted_password)


def _set_object_credential(
    config: Config,
    config_path: Path,
    obj_type: str,
    obj_name: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Set credentials for one inventory object of any type."""
    label = "cluster" if obj_type == "clusters" else f"{obj_type} object"
    section = config.data.get(obj_type, {})
    if obj_name not in section:
        available = list(section.keys())
        if obj_type == "clusters":
            hints = [f"Available clusters: {escape(', '.join(available))}"] if available else []
            raise CliError(f"Cluster '{obj_name}' not found in configuration.", hints=hints)
        hints = (
            [f"Available {obj_type}: {escape(', '.join(available))}"]
            if available
            else [f"No {obj_type} are defined in the configuration."]
        )
        raise CliError(f"{obj_type} object '{obj_name}' not found in configuration.", hints=hints)

    # Find and update the object's config file
    object_file = _find_object_file(config_path, obj_type, obj_name)
    if object_file is None:
        raise CliError(f"Could not find configuration file for {label} '{obj_name}'")

    try:
        _update_object_credentials(object_file, obj_type, obj_name, user, encrypted_password)
        print_success(f"Credentials updated for {label} '{obj_name}'")
        console.print(f"  File: {escape(str(object_file))}")
        console.print(f"  User: {escape(user)}")
        _print_password_status(encrypted_password)
    except Exception as e:
        raise CliError(f"Failed to update configuration: {e}") from e


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
        console.print(f"  File: {escape(str(users_file))}")
        console.print(f"  User: {escape(user)}")
        _print_password_status(encrypted_password)
    except Exception as e:
        raise CliError(f"Failed to update configuration: {e}") from e


def _print_password_status(encrypted_password: str) -> None:
    """Print password encryption status."""
    if encrypted_password.startswith("SOPS["):
        console.print("  Password: [dim](encrypted)[/dim]")
    else:
        console.print("  Password: [yellow](plain text)[/yellow]")


def _find_object_file(config_path: Path, obj_type: str, obj_name: str) -> Path | None:
    """Find the configuration file containing an inventory object.

    Looks in ``data/<obj_type>/*.toml``, then ``data/*.toml``, then any TOML
    file under the config directory whose ``[settings] type`` is ``data``.

    Args:
        config_path: Path to the configuration directory.
        obj_type: Inventory type (e.g., 'clusters', 'aiqums').
        obj_name: Name of the object to find.

    Returns:
        Path to the file, or None if not found.
    """
    import tomllib

    def _contains(toml_file: Path, require_data_type: bool) -> bool:
        try:
            with open(toml_file, "rb") as f:
                data = tomllib.load(f)
        except Exception:  # unreadable TOML files cannot contain the object
            return False
        if require_data_type and data.get("settings", {}).get("type") != "data":
            return False
        section = data.get(obj_type, {})
        return isinstance(section, dict) and obj_name in section

    type_dir = config_path / "data" / obj_type
    if type_dir.exists():
        for toml_file in type_dir.glob("*.toml"):
            if _contains(toml_file, False):
                return toml_file

    data_dir = config_path / "data"
    if data_dir.exists():
        for toml_file in data_dir.glob("*.toml"):
            if _contains(toml_file, False):
                return toml_file

    for toml_file in sorted(config_path.rglob("*.toml")):
        if _contains(toml_file, True):
            return toml_file

    return None


def _update_object_credentials(
    file_path: Path,
    obj_type: str,
    obj_name: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Update an inventory object's credentials in a TOML file.

    Args:
        file_path: Path to the TOML file.
        obj_type: Inventory type (e.g., 'clusters', 'aiqums').
        obj_name: Name of the object.
        user: Username to set.
        encrypted_password: Encrypted or plain password.
    """
    import tomllib

    import tomli_w

    # Read current content
    with open(file_path, "rb") as f:
        data = tomllib.load(f)

    # Update credentials
    if obj_type not in data:
        data[obj_type] = {}
    if obj_name not in data[obj_type]:
        data[obj_type][obj_name] = {}

    data[obj_type][obj_name]["user"] = user
    data[obj_type][obj_name]["enc"] = encrypted_password

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
