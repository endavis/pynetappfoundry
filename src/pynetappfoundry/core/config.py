"""Module to read configs and setup environment.

# return any items match all 3 tags
-f '{"bu":"Business", "env":"Prod", "tags":"active"}'
# return any item that matches bu and env and has both 'active' and 'workload' as a tag
-f '{"bu":"Business", "env":"Prod", "tags":"active && workload"}'
# return any item that matches bu, env, and tags and
#            app is one of app_name1 or app_name2
-f '{"bu":"Business", "app": "app_name1 || app_name2", "env":"Prod", "tags":"active"}'
# return any items with either name1 or name2
-f '{"name":"name1 || name2"}'

a data toml has the following section:
[settings]
type='data'

the following sections are valid in a data toml:
[aiqums]
[connectors]
[clusters]
[cloudinsights]
[azure]
[ibm]

This data is loaded into the Config.data attribute

And there are several ways to group this data into tomls:
1) A specific toml for each type of data
2) a toml for each distinct unit, like division, or bu

In addition, there are specific tomls
Azure settings (azure.toml)
IBM/Softlayer settings (ibm.toml)
AWS settings (aws.toml)
global settings (settings.toml)

These tomls are loading into the Config.config
    attribute by file name (without the .toml)

Scopes
A top-level directory of the config dir that contains a scope.toml marker is a
scope.  Its data files load into Config.data like any other, and Config.get_scope
records which scope each object came from.  Its users.toml, monitoring.toml and
consoleapi.toml (and no other settings file) load into a per-scope settings store
that lookups consult before the root.  Object names must be unique when either
copy is in a scope.  A config dir without scope.toml loads exactly as before.
See docs/reference/config-schema.md.
"""

from __future__ import annotations

import logging
import os
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from pynetappfoundry.core.models import (
    AIQUMAPISettings,
    ConsoleAPISettings,
    DIIAPISettings,
    LicensingSettings,
    ONTAPAPISettings,
    ScopeSettings,
    SMTPSettings,
)

_file_name = Path(__file__).name

T = TypeVar("T")


# Valid data types for config sections (used in data/*.toml files)
VALID_DATA_TYPES = frozenset(
    {
        "aiqums",
        "connectors",
        "clusters",
        "cloudinsights",
        "azure",
        "ibm",
    }
)

if TYPE_CHECKING:
    from pynetappfoundry.clients.trust import HostTrustStore


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid."""

    pass


# Settings fields that accept a ``SOPS[...]`` value (decrypted at read time).
_SMTP_SOPS_FIELDS = ("password",)
_DII_SOPS_FIELDS = ("api_ro_token",)
_CONSOLE_SOPS_FIELDS = ("client_secret", "service_token", "user_token")

# A top-level directory holding this file is a scope (see the module docstring).
SCOPE_MARKER = "scope.toml"
# The only settings files (by stem) a scope may contain; others are an error.
SCOPE_OVERRIDABLE_SETTINGS = frozenset({"users", "monitoring", "consoleapi"})
# The only Console [general] keys a scope inherits from the root consoleapi.toml.
_CONSOLE_INHERITED_KEYS = ("base_url", "ui_base_url", "base_api_path", "timeout")


def _read_tls_settings(source: Any, where: str) -> tuple[bool | None, str | None]:
    """Read and type-check ``verify_ssl`` / ``ca_bundle`` from one raw settings dict.

    Args:
        source: The raw dict (cluster entry or ``ontapapi.general``); anything that is
            not a dict counts as empty.
        where: Dotted prefix used in error messages, e.g. ``clusters.NAME``.

    Returns:
        ``(verify_ssl, ca_bundle)``, each ``None`` when unset.

    Raises:
        ConfigurationError: On a wrong type, or ``ca_bundle`` with ``verify_ssl = false``.
    """
    if not isinstance(source, Mapping):
        return None, None
    verify = source.get("verify_ssl")
    bundle = source.get("ca_bundle")
    if verify is not None and not isinstance(verify, bool):
        raise ConfigurationError(f"{where}.verify_ssl must be true or false, got {verify!r}.")
    if bundle is not None and (not isinstance(bundle, str) or not bundle.strip()):
        raise ConfigurationError(f"{where}.ca_bundle must be a non-empty path string.")
    if bundle is not None and verify is False:
        raise ConfigurationError(
            f"{where}.ca_bundle is set together with {where}.verify_ssl = false; "
            "remove one of them."
        )
    return verify, bundle


def _resolve_ca_bundle_path(bundle: str, config_dir: Path, key: str) -> str:
    """Return the absolute path of a CA bundle after checking it is a readable file.

    Raises:
        ConfigurationError: If the path is not an existing, readable regular file.
    """
    path = Path(bundle).expanduser()
    if not path.is_absolute():
        path = config_dir / path
    if not path.is_file():
        raise ConfigurationError(
            f"{key} is {str(path)!r}, which is not an existing CA bundle file."
        )
    if not os.access(path, os.R_OK):
        raise ConfigurationError(f"{key} is {str(path)!r}, which is not readable.")
    return str(path)


def resolve_tls_verify(
    config: Config,
    name: str,
    *,
    data_type: str = "clusters",
    settings_key: str = "ontapapi",
) -> bool | str:
    """Resolve the requests-style ``verify`` value for an API client.

    Precedence, first match wins: entry ``ca_bundle``, entry ``verify_ssl``,
    global ``ca_bundle``, global ``verify_ssl`` (``<settings_key>.toml``
    ``[general]``), then ``False``. Only the effective value is validated. Reads
    the raw dicts, so a missing settings file is not an error. The defaults
    resolve an ONTAP cluster; AIQUM passes ``data_type="aiqums"`` and
    ``settings_key="aiqumapi"``.

    Args:
        config: The loaded configuration. A non-dict ``data`` or ``settings`` counts
            as empty.
        name: Inventory entry to resolve for.
        data_type: Inventory section holding the entry (``clusters`` or ``aiqums``).
        settings_key: Key of the API settings in ``config.settings``.

    Returns:
        ``False`` (no chain validation; the fingerprint is pinned), ``True``
        (validate against requests' default bundle) or an absolute CA bundle path.

    Raises:
        ConfigurationError: On a wrong type, a contradiction, or an unusable bundle.
    """
    data = config.data if isinstance(config.data, dict) else {}
    settings = config.settings if isinstance(config.settings, dict) else {}
    section = data.get(data_type, {})
    cluster = section.get(name) if isinstance(section, Mapping) else None
    api_settings = settings.get(settings_key, {})
    general = api_settings.get("general") if isinstance(api_settings, dict) else None

    c_where = f"{data_type}.{name}"
    g_where = f"{settings_key}.general"
    c_verify, c_bundle = _read_tls_settings(cluster, c_where)
    config_dir = config.config_dir if isinstance(config.config_dir, Path) else Path.cwd()
    if c_bundle is not None:
        return _resolve_ca_bundle_path(c_bundle, config_dir, f"{c_where}.ca_bundle")
    if c_verify is not None:
        return c_verify
    g_verify, g_bundle = _read_tls_settings(general, g_where)
    if g_bundle is not None:
        return _resolve_ca_bundle_path(
            g_bundle,
            config_dir,
            f"{g_where}.ca_bundle ({data_type.removesuffix('s')} {name!r})",
        )
    return g_verify if g_verify is not None else False


class Config:
    """Configuration manager for TOML-based config files.

    Environment Variables:
        NF_<CLUSTER>_USER: Override username for a specific cluster.
        NF_<CLUSTER>_PASSWORD: Override password (base64 encoded) for a specific cluster.

    The cluster name in environment variables should be uppercase with hyphens
    replaced by underscores (e.g., cluster-prod -> NF_CLUSTER_PROD_USER).

    Note: The NF_CONFIG_DIR environment variable is handled by the CLI layer,
    not this class. Use `nf --config-dir` or set NF_CONFIG_DIR before running.
    """

    def __init__(
        self,
        config_dir: str | Path = "config",
        output_dir: str | Path = "",
        script_name: str = "",
        args: Any = None,
        *,
        no_cache: bool = False,
    ) -> None:
        """Initialize the configuration manager.

        Args:
            config_dir: Directory containing config files (relative to cwd or absolute).
                        Can be overridden by NF_CONFIG_DIR environment variable.
            output_dir: Directory for output files. If empty, uses data/{script_name}/output.
            script_name: Name of the calling script (used for directory naming).
            args: Optional parsed arguments object.
            no_cache: When True, every wrapped :class:`ClusterEntry` is built
                with ``no_cache=True``, causing ``.ontap`` accesses to bypass
                the cache database and fetch field groups live from the
                ONTAP API/CLI. Typically set via the ``--live`` CLI flag.
        """
        self.data: dict[str, dict[str, dict[str, Any]]] = {}
        self.args = args
        self.no_cache = no_cache
        self._trust_store: HostTrustStore | None = None
        # Memoized Console refresh token per scope (None = root): each SOPS decrypt
        # runs a subprocess.
        self._console_refresh_tokens: dict[str | None, str | None] = {}
        # Memoized SOPS plaintext keyed by ciphertext: each decrypt runs a subprocess.
        self._sops_plaintext: dict[str, str] = {}
        self.config_dir = Path.cwd() / config_dir
        self.data_types = ["aiqums", "connectors", "cloudinsights", "clusters", "azure", "ibm"]
        self.settings: dict[str, Any] = {}
        # Scopes (see the module docstring): markers, per-scope settings files, and
        # the scope and source file of every loaded data object.
        self.scopes: dict[str, ScopeSettings] = {}
        self.scope_settings: dict[str, dict[str, Any]] = {}
        self._object_scopes: dict[tuple[str, str], str | None] = {}
        self._object_sources: dict[tuple[str, str], Path | None] = {}
        self.parse_data()
        logging.debug(f"Toplevel settings: {list(self.settings.keys())}")
        self.script_name = script_name
        self.data_dir = Path(os.getcwd()) / "data" / script_name

        if output_dir:
            self.output_dir = Path(output_dir)
            self.db_dir = Path(output_dir)
        else:
            self.output_dir = self.data_dir / "output"
            self.db_dir = self.data_dir / "db"

        self.files_dir = self.data_dir / "files"
        self.log_dir = self.data_dir / "logs"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.files_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)

    def get_schema_location(self, api_name: str) -> Path:
        """Get the path to API schema files.

        Args:
            api_name: Name of the API (e.g., 'ontap', 'dii').

        Returns:
            Path to the API schema directory.
        """
        return Path(self.config_dir / "apis" / api_name)

    def get_scope(self, data_type: str, name: str) -> str | None:
        """Return the scope an inventory object belongs to.

        Args:
            data_type: Inventory section, e.g. ``clusters`` or ``connectors``.
            name: Object name.

        Returns:
            The scope (directory) name, or None for a root object or an unknown one.
        """
        return self._object_scopes.get((data_type, name))

    def console_account_scopes(self) -> list[str | None]:
        """Return the configured Console accounts (#1078, ADR-0028).

        Each scope with its own ``consoleapi.toml`` ``[general]`` table is a service
        account. The root is the default account, and counts only when it has
        credentials: its ``[general]`` has ``user_token``, ``service_token`` or
        ``client_id``, or a root refresh token resolves. A root that only carries
        the keys scopes inherit (``base_url`` and the like) is not an account.

        Returns:
            ``None`` for the root account when it counts, then the scope names
            that have a Console account, sorted.

        Raises:
            ConfigurationError: If the root refresh token is configured but cannot
                be resolved or decrypted.
        """
        accounts: list[str | None] = []
        root_general = self.settings.get("consoleapi", {}).get("general")
        has_credentials = isinstance(root_general, dict) and any(
            root_general.get(key) for key in ("user_token", "service_token", "client_id")
        )
        if has_credentials or self._resolve_console_refresh_token(None) is not None:
            accounts.append(None)
        accounts.extend(
            scope
            for scope in sorted(self.scopes)
            if self.scope_settings.get(scope, {}).get("consoleapi", {}).get("general") is not None
        )
        return accounts

    def _scope_tree(self, scope: str) -> dict[str, Any]:
        """Return the settings loaded from a scope's own files.

        Raises:
            ConfigurationError: If ``scope`` is not a known scope.
        """
        if scope not in self.scopes:
            available = ", ".join(sorted(self.scopes)) or "none"
            raise ConfigurationError(f"Unknown scope {scope!r} (available scopes: {available}).")
        return self.scope_settings.get(scope, {})

    @staticmethod
    def _walk(tree: Any, keys: tuple[str, ...]) -> tuple[bool, Any, str]:
        """Walk ``keys`` down ``tree``.

        Returns:
            ``(found, value, error)``; ``error`` describes why the walk failed.
        """
        current: Any = tree
        path_so_far: list[str] = []
        for key in keys:
            path_so_far.append(key)
            if not isinstance(current, dict):
                return (
                    False,
                    None,
                    f"Cannot access '{key}' in non-dict value at "
                    f"'{'.'.join(path_so_far[:-1])}'. "
                    "Check your configuration files.",
                )
            if key not in current:
                return (
                    False,
                    None,
                    f"Missing configuration key '{'.'.join(path_so_far)}'. "
                    f"Available keys at '{'.'.join(path_so_far[:-1]) or 'root'}': "
                    f"{list(current.keys())}. "
                    "Check your configuration files.",
                )
            current = current[key]
        return True, current, ""

    def get_setting(
        self, *keys: str, default: T | None = None, scope: str | None = None
    ) -> Any | T | None:
        """Get a nested setting value with a clear error message if not found.

        This method provides safe access to nested configuration values,
        avoiding KeyError exceptions with unhelpful messages.

        Args:
            *keys: Sequence of keys to traverse (e.g., 'ontapapi', 'general', 'base_api_path').
            default: Value to return if the key path doesn't exist. If None and key is missing,
                     raises ConfigurationError.
            scope: A scope name. The scope's own settings files (``users``,
                ``monitoring``, ``consoleapi``) are checked first; a path the
                scope does not set falls back to the root settings.

        Returns:
            The value at the specified key path, or the default value.

        Raises:
            ConfigurationError: If the key path doesn't exist and no default is provided,
                or ``scope`` is not a known scope.

        Example:
            >>> config.get_setting('ontapapi', 'general', 'base_api_path')
            '/api'
            >>> config.get_setting('missing', 'key', default='/default')
            '/default'
        """
        if scope is not None:
            found, value, _ = self._walk(self._scope_tree(scope), keys)
            if found:
                return value
        found, value, error = self._walk(self.settings, keys)
        if found:
            return value
        if default is not None:
            return default
        raise ConfigurationError(error)

    def get_object_setting(
        self, data_type: str, name: str, *keys: str, default: T | None = None
    ) -> Any | T | None:
        """Get a setting as seen by one inventory object, honouring its scope.

        Equivalent to ``get_setting(*keys, scope=get_scope(data_type, name))``, so
        a root object reads the root settings and a scoped object the scope's
        value first (for example a ``monitoring.toml`` threshold).
        """
        return self.get_setting(*keys, default=default, scope=self.get_scope(data_type, name))

    def get_smtp_settings(self) -> SMTPSettings:
        """Get SMTP settings for sending emails.

        Returns:
            SMTPSettings object with server configuration.

        Raises:
            ConfigurationError: If SMTP settings are not configured, or a
                ``SOPS[...]`` value cannot be decrypted.
        """
        try:
            smtp_data = self._decrypt_setting_fields(
                self.get_setting("settings", "SMTP"),
                _SMTP_SOPS_FIELDS,
                file="settings.toml",
                section="SMTP",
            )
            return SMTPSettings.model_validate(smtp_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid SMTP configuration: {e}. "
                "Ensure settings.toml has a valid [settings.SMTP] section with "
                "'server', 'port', 'user', 'password', and 'auth' fields."
            ) from e

    def get_ontap_api_settings(self) -> ONTAPAPISettings:
        """Get ONTAP REST API settings.

        Returns:
            ONTAPAPISettings object with API configuration.

        Raises:
            ConfigurationError: If ONTAP API settings are not configured.
        """
        try:
            ontap_data = self.get_setting("ontapapi", "general")
            return ONTAPAPISettings.model_validate(ontap_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid ONTAP API configuration: {e}. "
                "Ensure settings.toml has a valid [ontapapi.general] section "
                "with 'base_api_path' field."
            ) from e

    def get_dii_api_settings(self, name: str | None = None) -> DIIAPISettings:
        """Get Data Infrastructure Insights API settings.

        Args:
            name: Optional ``[cloudinsights.<name>]`` tenant. With a name, the
                tenant's ``base_url`` and token (see :meth:`get_secret`) override
                the ``diiapi.toml [general]`` values; everything else, and any
                value the tenant does not set, comes from ``[general]``.

        Returns:
            DIIAPISettings object with API configuration.

        Raises:
            ConfigurationError: If DII API settings are not configured, the tenant
                is unknown, or a ``SOPS[...]`` value cannot be decrypted.
        """
        try:
            general: Any = self.get_setting("diiapi", "general", default={})
            if name is None:
                dii_data = self._decrypt_setting_fields(
                    self.get_setting("diiapi", "general"),
                    _DII_SOPS_FIELDS,
                    file="diiapi.toml",
                    section="general",
                )
                return DIIAPISettings.model_validate(dii_data)

            tenants = self.data.get("cloudinsights", {})
            if name not in tenants:
                available = ", ".join(sorted(tenants)) or "none"
                raise ConfigurationError(
                    f"No Cloud Insights tenant named {name!r} in the [cloudinsights] "
                    f"inventory (available: {available})."
                )
            merged: dict[str, Any] = dict(general) if isinstance(general, dict) else {}
            tenant_url = tenants[name].get("base_url")
            if tenant_url:
                merged["base_url"] = tenant_url
            token = self.get_secret("cloudinsights", name)
            if token:
                merged["api_ro_token"] = token
            else:
                merged = self._decrypt_setting_fields(
                    merged, _DII_SOPS_FIELDS, file="diiapi.toml", section="general"
                )
            return DIIAPISettings.model_validate(merged)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid DII API configuration: {e}. "
                "Ensure settings.toml has a valid [diiapi.general] section with "
                "'api_ro_token', 'base_url', and 'base_api_path' fields."
            ) from e

    def get_aiqum_api_settings(self) -> AIQUMAPISettings:
        """Get Active IQ Unified Manager (AIQUM) REST API settings.

        Returns:
            AIQUMAPISettings object with API configuration.

        Raises:
            ConfigurationError: If ``aiqumapi.toml`` has no ``[general]`` section or
                it is invalid.
        """
        try:
            aiqum_data = self.get_setting("aiqumapi", "general")
            return AIQUMAPISettings.model_validate(aiqum_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid AIQUM API configuration: {e}. "
                "Ensure aiqumapi.toml has a valid [general] section "
                "(base_api_path, timeout)."
            ) from e

    def get_console_api_settings(self, *, scope: str | None = None) -> ConsoleAPISettings:
        """Get Console SaaS API settings.

        Args:
            scope: A scope name. The scope's Console account is strict: the scope
                needs its own ``consoleapi.toml``; only ``base_url``,
                ``ui_base_url``, ``base_api_path`` and ``timeout`` are inherited
                from the root ``[general]``. Credentials, ``org_id`` and
                ``agent_ids`` come only from the scope, and the refresh token only
                from the scope's ``users.toml [console]``.

        Returns:
            ConsoleAPISettings object with API configuration.

        Raises:
            ConfigurationError: If Console API settings are not configured, if
                ``consoleapi.toml`` carries a ``refresh_token`` (it belongs in
                ``users.toml [console]``), if ``scope`` is unknown or has no
                ``consoleapi.toml``, or if the refresh token or a
                ``SOPS[...]`` setting value cannot be decrypted.
        """
        try:
            console_file = "consoleapi.toml"
            if scope is None:
                console_data: dict[str, Any] = dict(self.get_setting("consoleapi", "general") or {})
            else:
                console_file = f"{scope}/consoleapi.toml"
                scope_general = self._scope_tree(scope).get("consoleapi", {}).get("general")
                if scope_general is None:
                    raise ConfigurationError(
                        f"Scope {scope!r} has no Console account: add {console_file} with a "
                        "[general] table. A scope never falls back to the root Console account."
                    )
                if not isinstance(scope_general, dict):
                    raise ConfigurationError(f"{console_file} [general] must be a table.")
                root_general = self.settings.get("consoleapi", {}).get("general")
                console_data = {}
                if isinstance(root_general, dict):
                    console_data = {
                        key: root_general[key]
                        for key in _CONSOLE_INHERITED_KEYS
                        if key in root_general
                    }
                console_data.update(scope_general)
            if "refresh_token" in console_data:
                raise ConfigurationError(
                    f"{console_file} must not contain 'refresh_token'. Store the Console "
                    "refresh token in users.toml under [console] ('enc'), for example with "
                    "'nf config set-credential --type console'."
                )
            console_data = self._decrypt_setting_fields(
                console_data,
                _CONSOLE_SOPS_FIELDS,
                file=console_file,
                section="general",
            )
            refresh_token = self._resolve_console_refresh_token(scope)
            if refresh_token is not None:
                console_data["refresh_token"] = refresh_token
            return ConsoleAPISettings.model_validate(console_data)
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(
                f"Invalid Console API configuration: {e}. "
                "Ensure consoleapi.toml has a valid [general] section with "
                "'base_url' and one of user_token, a refresh token (users.toml [console]), "
                "service_token or client_id/client_secret."
            ) from e

    def _resolve_console_refresh_token(self, scope: str | None = None) -> str | None:
        """Resolve the Console refresh token from ``users.toml [console]``.

        For the root, ``get_user("console", "console")`` decrypts SOPS values and
        applies the ``NF_CONSOLE_USER`` / ``NF_CONSOLE_PASSWORD`` overrides.  The
        ``user`` key is only a label and is never sent.  For a scope, only the
        scope's own ``users.toml [console]`` is read: there is no root fallback
        and the ``NF_CONSOLE_*`` variables are ignored.  The result is memoized
        per scope because each decrypt runs a ``sops`` subprocess.

        Args:
            scope: A scope name, or None for the root account.

        Returns:
            The decrypted refresh token, or None if none is configured.

        Raises:
            ConfigurationError: If the token cannot be resolved or decrypted.
                The message never includes the token or its ciphertext.
        """
        if scope in self._console_refresh_tokens:
            return self._console_refresh_tokens[scope]
        if scope is not None:
            token = self._resolve_scope_console_refresh_token(scope)
            self._console_refresh_tokens[scope] = token
            return token
        users = self.settings.get("users")
        configured = isinstance(users, dict) and "console" in users
        if not configured and not os.environ.get("NF_CONSOLE_PASSWORD"):
            self._console_refresh_tokens[None] = None
            return None
        try:
            _label, token = self.get_user("console", "console")
        except ConfigurationError as e:
            raise ConfigurationError(
                "Could not resolve the Console refresh token from users.toml [console] "
                "(or NF_CONSOLE_USER/NF_CONSOLE_PASSWORD); check the 'user' and 'enc' "
                "keys and, for a SOPS value, that sops and its key are available."
            ) from e
        self._console_refresh_tokens[None] = token
        return token

    def _resolve_scope_console_refresh_token(self, scope: str) -> str | None:
        """Read a scope's refresh token from its own ``users.toml [console]``.

        Raises:
            ConfigurationError: If the section lacks ``user`` or ``enc`` or the
                value cannot be decrypted. The message never includes the token.
        """
        users = self._scope_tree(scope).get("users")
        section = users.get("console") if isinstance(users, dict) else None
        if section is None:
            return None
        user = section.get("user") if isinstance(section, dict) else None
        enc = section.get("enc") if isinstance(section, dict) else None
        if not user or not enc or not isinstance(enc, str):
            raise ConfigurationError(
                f"Could not resolve the Console refresh token from {scope}/users.toml "
                "[console]; check the 'user' and 'enc' keys."
            )
        decrypted = self._decrypt_setting_fields(
            {"enc": enc}, ("enc",), file=f"{scope}/users.toml", section="console"
        )
        return str(decrypted["enc"])

    def get_licensing_settings(self) -> LicensingSettings | None:
        """Get licensing notification settings.

        Returns:
            LicensingSettings object if configured, None otherwise.
        """
        try:
            licensing_data = self.get_setting("settings", "licensing")
            return LicensingSettings.model_validate(licensing_data)
        except ConfigurationError:
            return None
        except Exception as e:
            logging.warning(f"Invalid licensing configuration: {e}")
            return None

    def parse_data(self) -> None:
        """Parse all TOML files in the config directory."""
        all_tomls = list(self.config_dir.rglob("*.toml"))
        self._load_scope_markers(all_tomls)
        loaded_tomls: list[Path] = []
        for file in all_tomls:
            if file.name == SCOPE_MARKER:
                continue
            logging.debug(f"{_file_name} : parsing {file}")
            scope = file.relative_to(self.config_dir).parts[0]
            self.parse_toml(file, scope=scope if scope in self.scopes else None)
            loaded_tomls.append(file)

        logging.debug(
            f"{_file_name} :loaded the"
            f" following files: {', '.join([str(path) for path in loaded_tomls])}"
        )
        self._wrap_clusters()
        self.add_searchable_keys()

    def _load_scope_markers(self, all_tomls: list[Path]) -> None:
        """Find and validate every ``scope.toml`` marker under the config dir.

        A marker is valid only directly inside a top-level, non-hidden directory
        that is not ``apis``.

        Raises:
            ConfigurationError: If a marker is anywhere else or is invalid.
        """
        for file in all_tomls:
            if file.name != SCOPE_MARKER:
                continue
            parts = file.relative_to(self.config_dir).parts
            if len(parts) != 2 or parts[0].startswith(".") or parts[0] == "apis":
                raise ConfigurationError(
                    f"{file}: {SCOPE_MARKER} is only valid directly inside a top-level "
                    "directory of the config dir (not at the root, nested deeper, or in "
                    "a hidden or 'apis' directory)."
                )
            self.scopes[parts[0]] = self._load_scope_marker(file)

    @staticmethod
    def _load_scope_marker(file: Path) -> ScopeSettings:
        """Validate one ``scope.toml`` marker.

        Raises:
            ConfigurationError: If the file is not valid TOML, has unknown keys or
                a ``name`` that differs from its directory name.
        """
        try:
            with open(file, "rb") as f:
                raw = tomllib.load(f)
            marker = ScopeSettings.model_validate(raw)
        except (tomllib.TOMLDecodeError, ValueError) as e:
            raise ConfigurationError(f"Invalid {file}: {e}") from e
        if marker.name is not None and marker.name != file.parent.name:
            raise ConfigurationError(
                f"{file}: name {marker.name!r} must equal the directory name "
                f"{file.parent.name!r} (or be omitted)."
            )
        return marker

    def get_trust_store(self) -> HostTrustStore:
        """Return the trust store for SSH host keys and TLS fingerprints.

        Records live under ``<config_dir>/.trust``. Built once and cached; nothing
        is created on disk until a record is written.
        """
        if self._trust_store is None:
            from pynetappfoundry.clients.trust import HostTrustStore

            self._trust_store = HostTrustStore(self.config_dir / ".trust")
        return self._trust_store

    def get_tls_verify(self, cluster_name: str) -> bool | str:
        """Return the TLS ``verify`` value for a cluster's ONTAP REST client.

        See :func:`resolve_tls_verify` for the precedence and errors.
        """
        return resolve_tls_verify(self, cluster_name)

    def _wrap_clusters(self) -> None:
        """Wrap each cluster config dict in a ClusterEntry.

        ClusterEntry provides a dict-like interface for backward compatibility
        and lazy per-namespace cache accessors (e.g. ``.ontap``, ``.occm``).
        """
        from pynetappfoundry.core.cluster_entry import ClusterEntry

        cache_db_path = self.config_dir / ".cache" / "cluster_metadata.db"
        clusters = self.data.get("clusters", {})
        for name, data in clusters.items():
            if not isinstance(data, ClusterEntry):
                clusters[name] = ClusterEntry(  # type: ignore[assignment]  # pyright: ignore[reportArgumentType]
                    name,
                    data,
                    cache_db_path,
                    config=self,
                    no_cache=self.no_cache,
                )

    def parse_toml(self, file: Path, *, scope: str | None = None) -> None:
        """Parse a single TOML file.

        Args:
            file: Path to the TOML file.
            scope: The scope directory the file is in, or None for the root.

        Raises:
            ConfigurationError: If a scoped settings file is not one a scope may
                override, or a scoped ``consoleapi.toml`` has more than ``[general]``.
        """
        with open(file, "rb") as f:
            data = tomllib.load(f)
            if (
                "settings" in data
                and "type" in data["settings"]
                and data["settings"]["type"] == "data"
            ):
                logging.debug(f"{_file_name} : data file: {file.stem}")
                self.load_data(data, source=file, scope=scope)
            elif scope is not None:
                logging.debug(f"{_file_name} : scope {scope} config file: {file.stem}")
                if file.stem not in SCOPE_OVERRIDABLE_SETTINGS:
                    raise ConfigurationError(
                        f"{file}: a scope may only contain the settings files "
                        f"{', '.join(sorted(f'{s}.toml' for s in SCOPE_OVERRIDABLE_SETTINGS))} "
                        f"(plus data files); {file.name!r} is not allowed in scope {scope!r}."
                    )
                if file.stem == "consoleapi" and set(data) - {"general"}:
                    raise ConfigurationError(
                        f"{file}: a scope's consoleapi.toml may only contain a [general] table."
                    )
                store = self.scope_settings.setdefault(scope, {})
                if file.stem not in store:
                    store[file.stem] = data
                else:
                    store[file.stem].update(data)
            else:
                logging.debug(f"{_file_name} : config file: {file.stem}")
                if file.stem not in self.settings:
                    self.settings[file.stem] = data
                else:
                    self.settings[file.stem].update(data)

    def _get_env_var_name(self, object_name: str) -> str:
        """Convert object name to environment variable format.

        Args:
            object_name: Name of the object (e.g., 'cluster-prod').

        Returns:
            Environment variable prefix (e.g., 'NF_CLUSTER_PROD').
        """
        # Replace hyphens with underscores and convert to uppercase
        return "NF_" + object_name.replace("-", "_").upper()

    def get_user(
        self, utype: str = "clusters", uobject: str = "", *, scope: str | None = None
    ) -> tuple[str, str]:
        """Get user credentials for a given type and object.

        Credentials are resolved in the following order (first found wins; each of
        user and password falls back independently):
        1. Environment variables: NF_<OBJECT>_USER and NF_<OBJECT>_PASSWORD
        2. Object-specific config in data files (e.g., clusters.toml)
        3. The object's scope's users.toml for the type (scoped objects only)
        4. Default credentials in the root users.toml for the type

        Args:
            utype: Type of object (e.g., 'clusters').
            uobject: Name of the specific object.
            scope: A scope to read defaults from; defaults to the object's own scope.

        Returns:
            Tuple of (username, encoded_password).

        Raises:
            ConfigurationError: If credentials cannot be found, or ``scope`` is unknown.
        """
        user: str | None = None
        enc: str | None = None
        eff_scope = scope if scope is not None else self.get_scope(utype, uobject)

        # 1. Check environment variables first (highest priority)
        if uobject:
            env_prefix = self._get_env_var_name(uobject)
            env_user = os.environ.get(f"{env_prefix}_USER")
            env_password = os.environ.get(f"{env_prefix}_PASSWORD")
            if env_user:
                logging.debug(f"Using user from {env_prefix}_USER")
                user = env_user
            if env_password:
                logging.debug(f"Using password from {env_prefix}_PASSWORD")
                enc = env_password

        # 2. Check object-specific config (if not already set by env vars)
        if not user or not enc:
            try:
                if not user:
                    user = self.data[utype][uobject]["user"]
                if not enc:
                    enc = self.data[utype][uobject]["enc"]
            except KeyError:
                pass

        # 3. The scope's own default credentials for the type
        if eff_scope is not None and (not user or not enc):
            scope_default = self._scope_tree(eff_scope).get("users", {}).get(utype)
            if isinstance(scope_default, dict):
                user = user or scope_default.get("user") or None
                enc = enc or scope_default.get("enc") or None

        # 4. Fall back to default credentials for the type
        if not user or not enc:
            try:
                if not user:
                    user = self.settings["users"][utype]["user"]
                if not enc:
                    enc = self.settings["users"][utype]["enc"]
            except KeyError:
                pass

        if not user:
            logging.error(f"Could not find user for {utype} and {uobject}")
            env_prefix = self._get_env_var_name(uobject) if uobject else "NF_<OBJECT>"
            raise ConfigurationError(
                f"Could not find user for type={utype!r}, object={uobject!r}. "
                f"Set {env_prefix}_USER environment variable, or configure in "
                "users.toml (root or the object's scope) or the object's data file."
            )
        if not enc:
            logging.error(f"Could not find password for {utype} and {uobject}")
            env_prefix = self._get_env_var_name(uobject) if uobject else "NF_<OBJECT>"
            raise ConfigurationError(
                f"Could not find password for type={utype!r}, object={uobject!r}. "
                f"Set {env_prefix}_PASSWORD environment variable, "
                "or configure 'enc' in config files."
            )

        # Decrypt SOPS-encrypted passwords
        password = self._decrypt_if_encrypted(enc, object_name=uobject)

        return user, password

    def get_secret(self, utype: str, uobject: str) -> str | None:
        """Get a token-style secret (no username) for a type and object.

        The secret is stored in the same ``enc`` field as a password. Order (first
        found wins):
        1. Environment variable ``NF_<OBJECT>_PASSWORD``
        2. ``enc`` on the object's data entry (``[<type>.<object>]``)
        3. ``enc`` in the object's scope ``users.toml [<type>]`` (scoped objects only)
        4. ``enc`` in the root ``users.toml [<type>]``

        Args:
            utype: Type of object (e.g., 'cloudinsights').
            uobject: Name of the specific object.

        Returns:
            The decrypted secret, or None if none is configured.

        Raises:
            ConfigurationError: If a ``SOPS[...]`` value cannot be decrypted. The
                message never includes the ciphertext or the plaintext.
        """
        value: Any = None
        section = f"{utype}.{uobject}"
        file = "the object's data file"
        env_value = os.environ.get(f"{self._get_env_var_name(uobject)}_PASSWORD") if uobject else ""
        if env_value:
            value = env_value
            file = "environment"
        else:
            entry = self.data.get(utype, {}).get(uobject)
            if isinstance(entry, dict) and entry.get("enc"):
                value = entry["enc"]
            else:
                scope = self.get_scope(utype, uobject)
                scope_users = self._scope_tree(scope).get("users") if scope is not None else None
                scope_default = scope_users.get(utype) if isinstance(scope_users, dict) else None
                users = self.settings.get("users")
                default = users.get(utype) if isinstance(users, dict) else None
                if isinstance(scope_default, dict) and scope_default.get("enc"):
                    value = scope_default["enc"]
                    file = f"{scope}/users.toml"
                    section = utype
                elif isinstance(default, dict) and default.get("enc"):
                    value = default["enc"]
                    file = "users.toml"
                    section = utype
        if not isinstance(value, str) or not value:
            return None
        decrypted = self._decrypt_setting_fields(
            {"enc": value}, ("enc",), file=file, section=section
        )
        return str(decrypted["enc"])

    def _decrypt_setting_fields(
        self, data: Any, fields: tuple[str, ...], *, file: str, section: str
    ) -> Any:
        """Decrypt ``SOPS[...]`` values of the listed fields of one settings section.

        Plaintext values pass through unchanged. Decrypted values are memoized per
        ``Config`` keyed by ciphertext. The raw ``self.settings`` is never modified.

        Args:
            data: The raw section; anything that is not a dict is returned as is.
            fields: Field names that may hold a ``SOPS[...]`` value.
            file: Settings file name, for error context.
            section: Section name, for error context.

        Returns:
            A shallow copy of ``data`` with the encrypted fields replaced by plaintext.

        Raises:
            ConfigurationError: If a value cannot be decrypted. The message never
                includes the ciphertext, the plaintext or the ``sops`` error text.
        """
        from pynetappfoundry.utils.sops import (
            SOPSError,
            SOPSNotInstalledError,
            decrypt_value,
            is_encrypted,
        )

        if not isinstance(data, dict):
            return data
        result = dict(data)
        for field in fields:
            value = result.get(field)
            if not isinstance(value, str) or not is_encrypted(value):
                continue
            cached = self._sops_plaintext.get(value)
            if cached is not None:
                result[field] = cached
                continue
            try:
                plaintext = decrypt_value(value)
            except SOPSError as e:
                logging.error(
                    f"Failed to decrypt SOPS value of {field!r} in {file} [{section}]: "
                    f"{type(e).__name__}"
                )
                reason = (
                    "sops is not installed"
                    if isinstance(e, SOPSNotInstalledError)
                    else "sops could not decrypt it; check that sops and your age key "
                    "(SOPS_AGE_KEY_FILE) are available"
                )
                raise ConfigurationError(
                    f"Failed to decrypt the SOPS value of '{field}' in {file} [{section}]: {reason}"
                ) from e
            self._sops_plaintext[value] = plaintext
            result[field] = plaintext
        return result

    def _decrypt_if_encrypted(self, value: str, object_name: str | None = None) -> str:
        """Decrypt a value if it is SOPS-encrypted.

        Args:
            value: The value to potentially decrypt.
            object_name: Cluster/object the value belongs to, for error context.

        Returns:
            Decrypted value if encrypted, otherwise the original value.

        Raises:
            ConfigurationError: If the value is SOPS-encrypted but decryption fails.
        """
        from pynetappfoundry.utils.sops import SOPSError, decrypt_value, is_encrypted

        if not is_encrypted(value):
            return value

        try:
            return decrypt_value(value)
        except SOPSError as e:
            logging.error(f"Failed to decrypt SOPS value for {object_name!r}: {e}")
            raise ConfigurationError(
                f"Failed to decrypt SOPS-encrypted password for object={object_name!r}: {e}"
            ) from e

    def count(self, section: str, id_field: str = "name") -> int:
        """Count unique items in a section.

        Args:
            section: The data section to count.
            id_field: The field to use for uniqueness.

        Returns:
            Number of unique items.
        """
        found: list[Any] = []
        for item in self.data[section]:
            try:
                found.append(getattr(item, id_field))
            except AttributeError:
                found.append(self.data[section][item][id_field])
        return len(set(found))

    def add_searchable_keys(self) -> None:
        """Add default searchable keys to data items."""
        for data_type in self.data_types:
            if (
                data_type in self.settings.get("settings", {})
                and "searchable_keys" in self.settings["settings"][data_type]
            ):
                default_keys = self.settings["settings"][data_type]["searchable_keys"]
                for item in self.data.get(data_type, {}):
                    if "name" not in self.data[data_type][item]:
                        self.data[data_type][item]["name"] = item
                    for key in default_keys:
                        if key not in self.data[data_type][item]:
                            self.data[data_type][item][key] = ""

    def get_relaxation_order(self, data_type: str) -> list[str]:
        """Get the key relaxation order for find_closest searches.

        The relaxation order determines which keys to remove first when
        progressively relaxing search criteria in find_closest().

        Priority:
        1. Explicit 'relaxation_order' in settings for the data type
        2. Reverse of 'searchable_keys' for the data type
        3. Default fallback order

        Args:
            data_type: The data type to get relaxation order for.

        Returns:
            List of keys in order of relaxation (first key removed first).
        """
        default_order = ["region", "subapp", "cloud", "env", "app", "bu", "div"]
        settings = self.settings.get("settings", {}).get(data_type, {})

        # Check for explicit relaxation_order
        if "relaxation_order" in settings:
            return list(settings["relaxation_order"])

        # Fall back to reverse of searchable_keys
        if "searchable_keys" in settings:
            return list(reversed(settings["searchable_keys"]))

        return default_order

    def load_data(
        self, data: dict[str, Any], *, source: Path | None = None, scope: str | None = None
    ) -> None:
        """Load data sections from a parsed TOML.

        Args:
            data: Parsed TOML data dictionary.
            source: The file the data came from, for error messages.
            scope: The scope the file is in, or None for the root.

        Raises:
            ConfigurationError: If an object name is already loaded and either
                copy is in a scope. Two root copies stay last-one-wins.
        """
        for data_type in self.data_types:
            if data_type not in self.data:
                self.data[data_type] = {}
            if data_type in data:
                logging.debug(f"{_file_name} : adding {len(data[data_type])} {data_type} items")
                for name in data[data_type]:
                    key = (data_type, name)
                    if key in self._object_sources and (
                        scope is not None or self._object_scopes[key] is not None
                    ):
                        raise ConfigurationError(
                            f"Duplicate {data_type} name {name!r} in "
                            f"{self._object_sources[key]} and {source}; "
                            "object names must be unique across scopes"
                        )
                    self._object_scopes[key] = scope
                    self._object_sources[key] = source
                self.data[data_type].update(data[data_type])

    def chk_and(self, search_term: str, values: list[str] | str) -> bool:
        """Check if an && (AND) condition matches.

        Args:
            search_term: Search term with && operators.
            values: Values to check against.

        Returns:
            True if all terms match.
        """
        # && only makes sense for lists
        if not isinstance(values, list):
            return False
        terms = [item.strip() for item in search_term.split(" && ")]
        return set(terms).issubset(values)

    def chk_or(self, search_term: str, value: list[str] | str) -> bool:
        """Check if an || (OR) condition matches.

        Args:
            search_term: Search term with || operators.
            value: Value to check against.

        Returns:
            True if any term matches.
        """
        terms = [item.strip() for item in search_term.split(" || ")]
        if isinstance(value, list):
            return any(item in value for item in terms)
        else:
            return any(item == value for item in terms)

    def check_term(self, term: str, value: list[str] | str) -> bool:
        """Check if a search term matches a value.

        Args:
            term: Search term (may contain && or ||).
            value: Value to check against.

        Returns:
            True if the term matches.
        """
        if " || " in term:
            return self.chk_or(term, value)
        elif " && " in term:
            return self.chk_and(term, value)
        else:
            if isinstance(value, list):
                return term in value
            else:
                return term == value

    def search(self, data_type: str, search_dict: dict[str, str]) -> dict[str, dict[str, Any]]:
        """Search for items that match the given fields.

        Each param should be a dictionary with field and value.
        This is case insensitive.

        Value can be {'tags':'active && Workload'} or
                     {'app': 'App1 || App2'}

        Args:
            data_type: Type of data to search (e.g., 'clusters').
            search_dict: Dictionary of field/value pairs to match.

        Returns:
            Dictionary of matching items.
        """
        if data_type not in self.data:
            return {}
        if not search_dict:
            return self.data[data_type].copy()
        logging.debug(f"{_file_name} :    search:")
        logging.debug(f"{_file_name} :     {data_type = }")
        logging.debug(f"{_file_name} :     {search_dict = }")
        results: dict[str, dict[str, Any]] = {}
        for item in self.data[data_type]:
            item_details = self.data[data_type][item]
            logging.debug(f"{_file_name} :      search: item - {item_details['name']}")
            result_check: list[bool] = []
            for key in search_dict:
                logging.debug(f"{_file_name} :      search: checking {key}")
                if key not in item_details:
                    result_check.append(False)
                    logging.debug(
                        f"{_file_name} :      search: {key} not in item details, did not match"
                    )
                    break
                logging.debug(
                    f"{_file_name} :      search: check_term {search_dict[key]}, "
                    f"{item_details[key]} returned "
                    f"{self.check_term(search_dict[key], item_details[key])}"
                )
                result_check.append(self.check_term(search_dict[key], item_details[key]))

            if all(result_check):
                logging.debug(f"{_file_name} :      search: item - {item_details['name']} matched")
                results[item] = item_details
            else:
                logging.debug(
                    f"{_file_name} :      search: item - {item_details['name']} did not match"
                )

        logging.debug(f"{_file_name} : search returned - {list(results.keys())}")
        return results

    def get_clusters(self, search_terms: dict[str, str]) -> dict[str, Any]:
        """Get clusters matching search terms.

        Args:
            search_terms: Dictionary of field/value pairs to match.

        Returns:
            Dictionary of matching clusters (ClusterEntry instances).
        """
        return self.search("clusters", search_terms)

    def find_closest(self, data_type: str, tree: dict[str, str]) -> dict[str, Any] | None:
        """Find the closest matching item by progressively relaxing search criteria.

        The order in which keys are relaxed (removed) is determined by:
        1. Explicit 'relaxation_order' in settings for the data type
        2. Reverse of 'searchable_keys' for the data type
        3. Default fallback order

        Args:
            data_type: Type of data to search.
            tree: Dictionary of hierarchical search criteria.

        Returns:
            The closest matching item, or None if not found.
        """
        logging.debug(f"{_file_name} :find_closest")
        logging.debug(f"{_file_name} :  {data_type = }")
        logging.debug(f"{_file_name} :  {tree = }")
        tree = tree.copy()
        key_order = self.get_relaxation_order(data_type)
        found: dict[str, Any] | None = None

        # remove empty keys
        for key in key_order:
            if key in tree and tree[key] == "":
                del tree[key]

        logging.debug(f"{_file_name} :  initial search {tree = }")
        # try matching tree as is
        results = self.search(data_type, tree)
        if len(results) == 1:
            found = results.popitem()[1]

        else:
            # go through the key_order and delete keys until something is found
            for key in key_order:
                if key in tree:
                    logging.debug(f"{_file_name} :  removing {key} and searching {tree = }")
                    del tree[key]
                else:
                    continue
                if tree:
                    results = self.search(data_type, tree)
                    logging.debug(f"{_file_name} :  search_returned {results}")
                    if len(results) == 1:
                        found = results.popitem()[1]
                        break

        logging.debug(f"{_file_name} : find_closest - {found = }")
        return found
