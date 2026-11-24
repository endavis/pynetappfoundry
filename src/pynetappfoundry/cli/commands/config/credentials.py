"""Credential management commands."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.markup import escape

from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.utils import print_success, print_warning
from pynetappfoundry.core.config import (
    SCOPE_OVERRIDABLE_SETTINGS,
    SOPS_SETTING_TARGETS,
    VALID_DATA_TYPES,
    Config,
    ConfigurationError,
)
from pynetappfoundry.core.settings_files import find_setting_file, write_toml_values
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


def _encrypt_setting_value(value: str) -> str:
    """Encrypt a setting value into a ``SOPS[...]`` string; there is no plain text fallback.

    Args:
        value: The plain text secret.

    Returns:
        The ``SOPS[...]`` string.

    Raises:
        CliError: If sops or the age key is missing, or encryption fails.
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
    return encrypted


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
        "'console' stores the Console refresh token (not the client secret; use "
        "--setting consoleapi.client_secret for that): --user is only a label and "
        "the password prompt takes the refresh token."
    ),
)
@click.option(
    "--setting",
    type=click.Choice(sorted(SOPS_SETTING_TARGETS)),
    help=(
        "Store one SOPS-encrypted setting as <file>.<field>, for example "
        "consoleapi.client_secret. Cannot be combined with --cluster, --type, "
        "--name, --user or --no-encrypt; the value is prompted (hidden) or "
        "taken from --password. Only consoleapi.* accepts --scope."
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
    "--scope",
    help=(
        "Write to this scope's users.toml (a top-level directory with a scope.toml). "
        "With --cluster or --name it must equal the object's own scope."
    ),
)
@click.option(
    "--user",
    help="Username (required with --cluster and --type).",
)
@click.option(
    "--password",
    help="Password or value (will prompt, hidden, if not provided).",
)
@click.option(
    "--no-encrypt",
    is_flag=True,
    help="Store password as plain text (not recommended).",
)
@click.option(
    "--read-write",
    "read_write",
    is_flag=True,
    help=(
        "Store the value as a Cloud Insights tenant's own read-write key (rw_enc on "
        "its data entry). Requires --type cloudinsights and --name; takes no --user. "
        "The key is prompted (hidden) or taken from --password."
    ),
)
@click.pass_context
def set_credential(
    ctx: click.Context,
    cluster: str | None,
    cred_type: str | None,
    setting: str | None,
    obj_name: str | None,
    scope: str | None,
    user: str | None,
    password: str | None,
    no_encrypt: bool,
    read_write: bool,
) -> None:
    """Set encrypted credentials for an inventory object, a resource type or a setting.

    Use --type with --name to set credentials for one object of any inventory
    type (stored on its data file entry); --cluster NAME is an alias for
    --type clusters --name NAME.
    Use --type alone to set default credentials for all resources of a type
    (stored in users.toml).
    Use --setting FILE.FIELD to store one SOPS-encrypted secret of a settings
    file, such as the Console client secret.

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

        # Store that tenant's own read-write key (for DII writes)
        nf config set-credential --type cloudinsights --name tenant1 --read-write

        # Set default credentials for all clusters
        nf config set-credential --type clusters --user admin

        # Store the Console refresh token (the user is a label, never sent;
        # the password prompt takes the refresh token)
        nf config set-credential --type console --user console

        # Set default credentials for the clusters of one scope (Org1/users.toml)
        nf config set-credential --type clusters --scope Org1 --user admin

        # Store one scope's Console refresh token (Org1/users.toml)
        nf config set-credential --type console --scope Org1 --user console

        # Store the Console client secret (consoleapi.toml [general])
        nf config set-credential --setting consoleapi.client_secret

        # Store one scope's Console client secret (Org1/consoleapi.toml)
        nf config set-credential --setting consoleapi.client_secret --scope Org1

        # Store the DII API token or the SMTP password
        nf config set-credential --setting diiapi.api_ro_token
        nf config set-credential --setting diiapi.api_rw_token
        nf config set-credential --setting digitaladvisorapi.refresh_token
        nf config set-credential --setting settings.smtp_password
    """
    if setting is not None:
        _check_setting_options(cluster, cred_type, obj_name, user, no_encrypt, read_write)
        _run_setting(ctx, setting, scope, password)
        return

    if read_write:
        _run_read_write(ctx, cluster, cred_type, obj_name, scope, user, password, no_encrypt)
        return

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

    if user is None:
        raise click.UsageError("Missing option '--user'.")

    config_path, config = _load_config(ctx)

    # Check --scope before prompting for or encrypting anything
    if scope is not None:
        _check_scope_option(config, scope, cluster, cred_type, obj_name)

    # Prompt for the password only after every check passed
    if password is None:
        password = _prompt_secret("Password")

    # Encrypt password
    encrypted_password = _encrypt_password(password, no_encrypt, ctx)

    if cluster:
        _set_object_credential(config, config_path, "clusters", cluster, user, encrypted_password)
    elif obj_name:
        assert cred_type is not None  # For type checker
        _set_object_credential(config, config_path, cred_type, obj_name, user, encrypted_password)
    else:
        assert cred_type is not None  # For type checker
        _set_type_credential(config, config_path, cred_type, user, encrypted_password, scope)


def _load_config(ctx: click.Context) -> tuple[Path, Config]:
    """Locate the configuration directory and load it.

    Raises:
        CliError: If the directory is missing or fails to load.
    """
    config_dir = ctx.obj.get("config_dir", "config")
    config_path = Path.cwd() / config_dir

    if not config_path.exists():
        raise CliError(f"Configuration directory not found: {config_path}")

    try:
        config = Config(config_dir=config_dir, script_name="set-credential")
    except Exception as e:
        raise CliError(f"Failed to load configuration: {e}") from e
    return config_path, config


def _prompt_secret(label: str) -> str:
    """Prompt for a hidden value, asking twice."""
    return str(click.prompt(label, hide_input=True, confirmation_prompt=True))


def _check_setting_options(
    cluster: str | None,
    cred_type: str | None,
    obj_name: str | None,
    user: str | None,
    no_encrypt: bool,
    read_write: bool = False,
) -> None:
    """Reject options that cannot be combined with ``--setting``.

    Raises:
        CliError: Naming every option given that conflicts.
    """
    given = [
        flag
        for flag, present in (
            ("--cluster", cluster is not None),
            ("--type", cred_type is not None),
            ("--name", obj_name is not None),
            ("--user", user is not None),
            ("--no-encrypt", no_encrypt),
            ("--read-write", read_write),
        )
        if present
    ]
    if given:
        raise CliError(
            f"--setting cannot be combined with {', '.join(given)}.",
            hints=[
                "--setting stores one SOPS secret; only --scope (consoleapi.* targets) "
                "and --password (the value) are allowed with it."
            ],
        )


_READ_WRITE_HINT = "nf config set-credential --type cloudinsights --name <tenant> --read-write"


def _run_read_write(
    ctx: click.Context,
    cluster: str | None,
    cred_type: str | None,
    obj_name: str | None,
    scope: str | None,
    user: str | None,
    password: str | None,
    no_encrypt: bool,
) -> None:
    """Store a Cloud Insights tenant's own read-write key; every check runs before any prompt."""
    hints = [f"Run '{_READ_WRITE_HINT}'."]
    if cluster is not None:
        raise CliError("--read-write cannot be combined with --cluster.", hints=hints)
    if cred_type != "cloudinsights":
        raise CliError("--read-write requires --type cloudinsights.", hints=hints)
    if obj_name is None:
        raise CliError("--read-write requires --name <tenant>.", hints=hints)
    if user is not None:
        raise CliError(
            "--read-write takes no --user; the key has no username.",
            hints=hints,
        )
    config_path, config = _load_config(ctx)
    if scope is not None:
        _check_scope_option(config, scope, None, cred_type, obj_name)
    object_file = _object_file_or_error(config, config_path, cred_type, obj_name)
    if password is None:
        password = _prompt_secret("Read-write key")
    encrypted = _encrypt_password(password, no_encrypt, ctx)
    _set_tenant_rw_key(object_file, obj_name, encrypted)


def _set_tenant_rw_key(object_file: Path, name: str, encrypted: str) -> None:
    """Write ``rw_enc`` on a tenant's data entry; never prints the value."""
    try:
        _write_toml_values(object_file, ["cloudinsights", name], {"rw_enc": encrypted})
    except Exception as e:
        raise CliError(f"Failed to update configuration: {e}") from e
    print_success(f"Read-write key stored for cloudinsights object '{name}'")
    console.print(f"  File: {escape(str(object_file))}")
    _print_password_status(encrypted, label="Read-write key")


def _run_setting(ctx: click.Context, setting: str, scope: str | None, value: str | None) -> None:
    """Store one SOPS-encrypted setting; every check runs before the value is prompted."""
    config_path, config = _load_config(ctx)
    stem = SOPS_SETTING_TARGETS[setting][0]
    if scope is not None:
        _check_setting_scope(config, scope, stem)
    target_file = _find_setting_file(config_path, stem, scope)
    if value is None:
        value = _prompt_secret("Value")
    encrypted = _encrypt_setting_value(value)
    _set_setting_value(target_file, setting, scope, encrypted)


def _check_setting_scope(config: Config, scope: str, stem: str) -> None:
    """Validate ``--scope`` for a ``--setting`` target.

    Raises:
        CliError: If the scope is unknown or its file may not live in a scope.
    """
    _scope_tree_or_error(config, scope)
    if stem not in SCOPE_OVERRIDABLE_SETTINGS:
        allowed = ", ".join(f"{s}.toml" for s in sorted(SCOPE_OVERRIDABLE_SETTINGS))
        raise CliError(
            f"{stem}.toml cannot be set per scope; a scope may only hold {allowed}.",
            hints=["Drop --scope, or use a consoleapi.* target."],
        )


def _scope_tree_or_error(config: Config, scope: str) -> dict[str, Any]:
    """Return a scope's settings, turning an unknown scope into a CliError."""
    try:
        return config.get_scope_settings(scope)
    except ConfigurationError as e:
        raise CliError(str(e)) from e


def _check_scope_option(
    config: Config,
    scope: str,
    cluster: str | None,
    cred_type: str | None,
    obj_name: str | None,
) -> None:
    """Validate ``--scope`` against the other options before anything is written.

    A scope must exist. With an object (``--cluster`` or ``--name``) it must also
    equal the object's own scope; credentials for an object live in its data file.
    """
    _scope_tree_or_error(config, scope)
    name = cluster or obj_name
    if name is None:
        return
    obj_type = "clusters" if cluster else str(cred_type)
    if name not in config.data.get(obj_type, {}):
        return  # the "not found" error is raised by _set_object_credential
    real_scope = config.get_scope(obj_type, name)
    if real_scope != scope:
        where = f"scope '{real_scope}'" if real_scope else "the root (no scope)"
        raise CliError(
            f"{obj_type} object '{name}' is in {where}, not scope '{scope}'.",
            hints=[f"Use --scope {real_scope}." if real_scope else "Drop --scope."],
        )


def _set_object_credential(
    config: Config,
    config_path: Path,
    obj_type: str,
    obj_name: str,
    user: str,
    encrypted_password: str,
) -> None:
    """Set credentials for one inventory object of any type.

    ``--scope`` was already checked against the object by ``_check_scope_option``.
    """
    label = "cluster" if obj_type == "clusters" else f"{obj_type} object"
    object_file = _object_file_or_error(config, config_path, obj_type, obj_name)

    try:
        _update_object_credentials(object_file, obj_type, obj_name, user, encrypted_password)
        print_success(f"Credentials updated for {label} '{obj_name}'")
        console.print(f"  File: {escape(str(object_file))}")
        console.print(f"  User: {escape(user)}")
        _print_password_status(encrypted_password)
    except Exception as e:
        raise CliError(f"Failed to update configuration: {e}") from e


def _object_file_or_error(config: Config, config_path: Path, obj_type: str, obj_name: str) -> Path:
    """Return the data file of one inventory object.

    Raises:
        CliError: If the object is unknown or its file cannot be found.
    """
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
    return object_file


def _set_type_credential(
    config: Config,
    config_path: Path,
    cred_type: str,
    user: str,
    encrypted_password: str,
    scope: str | None = None,
) -> None:
    """Set default credentials for a resource type in users.toml.

    With ``scope`` the credentials go to ``<config>/<scope>/users.toml`` instead
    of the root file, creating it when missing.
    """
    users_file = config_path / "users.toml"
    scope_note = ""
    if scope is not None:
        tree = _scope_tree_or_error(config, scope)
        users_file = config_path / scope / "users.toml"
        scope_note = f" in scope '{scope}'"
        if cred_type == "console" and "general" not in tree.get("consoleapi", {}):
            print_warning(
                f"Scope '{scope}' has no Console account ([general] in "
                f"{scope}/consoleapi.toml); the token is stored but not used until it does."
            )

    try:
        _update_users_credentials(users_file, cred_type, user, encrypted_password)
        if cred_type == "console":
            print_success(f"Refresh token stored{scope_note}")
        else:
            print_success(f"Default credentials updated for type '{cred_type}'{scope_note}")
        console.print(f"  File: {escape(str(users_file))}")
        console.print(f"  User: {escape(user)}")
        _print_password_status(
            encrypted_password, label="Refresh token" if cred_type == "console" else "Password"
        )
    except Exception as e:
        raise CliError(f"Failed to update configuration: {e}") from e

    if cred_type == "console":
        scope_arg = f" --scope {scope}" if scope is not None else ""
        console.print(
            "  This is the refresh token, not the client secret. Store the client secret with: "
            f"nf config set-credential --setting consoleapi.client_secret{escape(scope_arg)}"
        )


def _print_password_status(encrypted_password: str, label: str = "Password") -> None:
    """Print password encryption status."""
    if encrypted_password.startswith("SOPS["):
        console.print(f"  {label}: [dim](encrypted)[/dim]")
    else:
        console.print(f"  {label}: [yellow](plain text)[/yellow]")


def _set_setting_value(
    target_file: Path, setting: str, scope: str | None, encrypted_value: str
) -> None:
    """Write an encrypted value to ``target_file``, in the table ``setting`` names.

    Prints the target and the counterpart warnings; never the value.
    """
    stem, table, key = SOPS_SETTING_TARGETS[setting]
    created = not target_file.exists()

    try:
        leaf = _write_toml_values(target_file, [table], {key: encrypted_value})
    except Exception as e:
        raise CliError(f"Failed to update configuration: {e}") from e

    scope_note = f" in scope '{scope}'" if scope is not None else ""
    print_success(f"Setting {setting} stored{scope_note}")
    console.print(f"  File: {escape(str(target_file))}")
    console.print(f"  Table: {escape(table)}")
    console.print(f"  Key: {escape(key)}")
    console.print("  Value: [dim](encrypted)[/dim]")

    if created and stem == "consoleapi":
        print_warning(
            f"Created {target_file}; the Console account still needs client_id and org_id."
        )
    elif key == "client_secret" and not leaf.get("client_id"):
        print_warning(f"{target_file} has no client_id; the Console account needs one.")
    elif setting == "settings.smtp_password" and not leaf.get("user"):
        print_warning(f"{target_file} [{table}] has no user; set it for SMTP authentication.")


def _find_setting_file(config_path: Path, stem: str, scope: str | None) -> Path:
    """Pick the settings file a ``--setting`` target is written to.

    See :func:`pynetappfoundry.core.settings_files.find_setting_file`.

    Raises:
        CliError: If more than one file carries the stem.
    """
    try:
        return find_setting_file(config_path, stem, scope)
    except ConfigurationError as e:
        raise CliError(
            str(e),
            hints=["The loader merges them, so the file to write is ambiguous. Keep one."],
        ) from e


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
    _write_toml_values(file_path, [obj_type, obj_name], {"user": user, "enc": encrypted_password})


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
    _write_toml_values(users_file, [cred_type], {"user": user, "enc": encrypted_password})


_write_toml_values = write_toml_values
