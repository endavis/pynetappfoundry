"""Static configuration checks that return structured results.

The checks read the loaded :class:`~pynetappfoundry.core.config.Config` and, where a
credential must be proven present, decrypt SOPS values locally. They make no network
call and never put a secret, plaintext or ciphertext, in a result. They import
neither Rich nor click, so ``nf config validate`` renders the results and other
callers (such as ``nf doctor``) can reuse them. See ADR-0034.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ValidationError

from pynetappfoundry._version import __version__
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.models import (
    AIQUMConfig,
    CloudInsightsConfig,
    ClusterConfig,
    ConnectorConfig,
    UserCredentials,
)

CONFIG_SCHEMA_DOC = "docs/reference/config-schema.md"
CONFIGURATION_DOC = "docs/getting-started/configuration.md"

# Credential types ``nf config set-credential --type`` accepts.
CREDENTIAL_TYPES = (
    "aiqums",
    "azure",
    "cloudinsights",
    "clusters",
    "connectors",
    "console",
    "ibm",
)


class CheckStatus(StrEnum):
    """Outcome of one check."""

    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class CheckResult:
    """One checked item.

    Attributes:
        subject: What was checked, such as ``clusters.c1`` or ``spec.ontap``.
        status: Outcome. Only ``error`` fails validation.
        label: Plain row text (not markup).
        errors: The exact error-panel lines; non-empty only for ``error``.
        hint: Plain advice on how to fix or complete the item, or None.
        hint_as_sibling: Draw the hint as a row beside this one instead of nested
            under it. Only the Console refresh-token hint does, to keep its
            long-standing output.
    """

    subject: str
    status: CheckStatus
    label: str
    errors: tuple[str, ...] = ()
    hint: str | None = None
    hint_as_sibling: bool = False


@dataclass(frozen=True)
class CheckSection:
    """A titled group of results."""

    title: str
    results: tuple[CheckResult, ...]


# (display name, API, spec file name, where to copy it from in the repository)
SPEC_FILES: tuple[tuple[str, str, str, str], ...] = (
    ("ONTAP", "ontap", "all.json", "docs/example-config/apis/ontap/all.json"),
    ("AIQUM", "aiqum", "all.json", "docs/example-config/apis/aiqum/all.json"),
    ("DII", "dii", "all.json", "docs/example-config/apis/dii/all.json"),
    (
        "Console",
        "console",
        "console_openapi.yaml",
        "tools/console_openapi/generated/console_openapi.yaml",
    ),
)


def _in_scope(config: Config, data_type: str, scope: str | None) -> dict[str, Any]:
    """Return the ``data_type`` objects to check: all of them, or only those of ``scope``."""
    objects: dict[str, Any] = config.data.get(data_type, {})
    if scope is None:
        return objects
    return {
        name: data for name, data in objects.items() if config.get_scope(data_type, name) == scope
    }


def _error_lines(prefix: str, error: ValidationError) -> tuple[str, ...]:
    """Format a pydantic error as ``<prefix>.<field>: <message>`` lines."""
    return tuple(
        f"{prefix}.{'.'.join(str(x) for x in err['loc'])}: {err['msg']}" for err in error.errors()
    )


def _check_entries(
    data_type: str,
    model: type[BaseModel],
    entries: dict[str, Any],
    *,
    require_ip: bool = False,
) -> list[CheckResult]:
    """Validate each inventory entry against ``model``."""
    results: list[CheckResult] = []
    for name, data in entries.items():
        subject = f"{data_type}.{name}"
        hint = f"Fix the field in the data file that defines [{data_type}.{name}]."
        try:
            model.model_validate(data)
        except ValidationError as e:
            results.append(
                CheckResult(
                    subject, CheckStatus.ERROR, f"{name}: Invalid", _error_lines(subject, e), hint
                )
            )
            continue
        if require_ip and not (isinstance(data, dict) and data.get("ip")):
            results.append(
                CheckResult(
                    subject,
                    CheckStatus.ERROR,
                    f"{name}: Invalid",
                    (f"{subject}.ip: ip is required",),
                    f"Add an ip to [{data_type}.{name}] in its data file.",
                )
            )
            continue
        results.append(CheckResult(subject, CheckStatus.OK, str(name)))
    return results


def check_clusters(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Validate the cluster entries.

    Args:
        config: Config instance to check.
        scope: Check only this scope's clusters; None checks every cluster.
    """
    clusters = _in_scope(config, "clusters", scope)
    if not clusters:
        return [CheckResult("clusters", CheckStatus.WARNING, "No clusters configured")]
    return _check_entries("clusters", ClusterConfig, clusters)


def check_users(
    users: dict[str, Any], *, label_prefix: str = "users", scope: str | None = None
) -> list[CheckResult]:
    """Validate the ``users.toml`` credential tables.

    Args:
        users: The parsed ``users.toml`` sections.
        label_prefix: Prefix of each error key, ``users`` or ``<scope>/users``.
        scope: The scope the file belongs to, or None for the root file.
    """
    if not users:
        return [CheckResult("users", CheckStatus.WARNING, "No users configured")]
    file = "users.toml" if scope is None else f"{scope}/users.toml"
    scope_arg = "" if scope is None else f" --scope {scope}"
    results: list[CheckResult] = []
    for utype, udata in users.items():
        if not (isinstance(udata, dict) and "user" in udata):
            continue
        try:
            UserCredentials.model_validate(udata)
        except ValidationError as e:
            hint = f"Fix [{utype}] in {file}: it needs 'user' and 'enc'."
            if utype in CREDENTIAL_TYPES:
                hint += (
                    f" Rewrite it with: nf config set-credential --type {utype}{scope_arg}"
                    " --user USER"
                )
            results.append(
                CheckResult(
                    f"users.{utype}",
                    CheckStatus.ERROR,
                    f"{utype}: Invalid",
                    _error_lines(f"{label_prefix}.{utype}", e),
                    hint,
                )
            )
        else:
            results.append(CheckResult(f"users.{utype}", CheckStatus.OK, str(utype)))
    return results


def _settings_result(
    config: Config,
    *,
    label: str,
    keys: tuple[str, str],
    reader: Callable[[], object],
    absent: CheckResult,
    tree: dict[str, Any] | None = None,
    error_prefix: str = "",
    hint: Callable[[], str | None] | None = None,
) -> CheckResult:
    """Report one settings section as valid, not configured, or invalid.

    A section that is absent is "not configured" (``absent``). A section that is
    present but fails to load (invalid fields, a SOPS value that cannot be
    decrypted) is an error carrying the reader's message.
    """
    top = (config.settings if tree is None else tree).get(keys[0])
    if not isinstance(top, dict) or keys[1] not in top:
        return absent
    subject = ".".join(keys)
    try:
        reader()
    except ConfigurationError as e:
        specific = hint() if hint is not None else None
        return CheckResult(
            subject,
            CheckStatus.ERROR,
            f"{label}: Invalid",
            (f"{error_prefix}{subject}: {e}",),
            specific or f"See {CONFIG_SCHEMA_DOC} ({subject}).",
            hint_as_sibling=specific is not None,
        )
    return CheckResult(subject, CheckStatus.OK, label)


def _refresh_token_hint(
    general: object, users: object, scope: str | None, file_name: str
) -> str | None:
    """Explain a Console account that has a ``client_id`` but no ``client_secret``.

    The usual cause is a client secret stored as a refresh token in ``users.toml``
    ``[console]``. Returns plain advice, or None when it does not apply.

    Args:
        general: The raw ``[general]`` table of the ``consoleapi.toml`` in question.
        users: The raw ``users.toml`` sections of the same root or scope.
        scope: The scope name, or None for the root.
        file_name: Display name of the ``consoleapi.toml`` file.
    """
    if (
        not isinstance(general, dict)
        or not general.get("client_id")
        or general.get("client_secret")
    ):
        return None
    console_entry = users.get("console") if isinstance(users, dict) else None
    if not isinstance(console_entry, dict) or not console_entry.get("enc"):
        return None
    scope_arg = f" --scope {scope}" if scope else ""
    return (
        f"{file_name} has client_id but no client_secret. The secret was probably stored "
        "as a refresh token in users.toml [console]. Store it with: "
        f"nf config set-credential --setting consoleapi.client_secret{scope_arg}"
    )


def _aiqum_api_result(config: Config) -> CheckResult | None:
    """The ``AIQUM API`` row: shown only when AIQUM is in use."""
    aiqumapi = config.settings.get("aiqumapi")
    has_general = isinstance(aiqumapi, dict) and "general" in aiqumapi
    if not has_general and not config.data.get("aiqums"):
        return None
    if has_general:
        return _settings_result(
            config,
            label="AIQUM API",
            keys=("aiqumapi", "general"),
            reader=config.get_aiqum_api_settings,
            absent=CheckResult(
                "aiqumapi.general", CheckStatus.SKIPPED, "AIQUM API: Not configured"
            ),
        )
    return CheckResult(
        "aiqumapi.general",
        CheckStatus.ERROR,
        "AIQUM API: Not configured",
        (
            "aiqumapi.general: aiqumapi.toml has no [general] section, "
            "required by the [aiqums] inventory",
        ),
        f"Create <config>/apis/aiqum/aiqumapi.toml with a [general] section; see "
        f"{CONFIG_SCHEMA_DOC} (aiqumapi).",
    )


def check_settings(config: Config) -> list[CheckResult]:
    """Validate the root settings files."""
    results = [
        _settings_result(
            config,
            label="ONTAP API",
            keys=("ontapapi", "general"),
            reader=config.get_ontap_api_settings,
            absent=CheckResult(
                "ontapapi.general", CheckStatus.WARNING, "ONTAP API: Not configured"
            ),
        ),
        _settings_result(
            config,
            label="DII API",
            keys=("diiapi", "general"),
            reader=config.get_dii_api_settings,
            absent=CheckResult(
                "diiapi.general", CheckStatus.SKIPPED, "DII API: Not configured (optional)"
            ),
        ),
    ]
    results.append(
        _settings_result(
            config,
            label="Digital Advisor API",
            keys=("digitaladvisorapi", "general"),
            reader=config.get_digital_advisor_api_settings,
            absent=CheckResult(
                "digitaladvisorapi.general",
                CheckStatus.SKIPPED,
                "Digital Advisor API: Not configured (optional)",
            ),
        )
    )
    aiqum = _aiqum_api_result(config)
    if aiqum is not None:
        results.append(aiqum)
    results.append(
        _settings_result(
            config,
            label="SMTP",
            keys=("settings", "SMTP"),
            reader=config.get_smtp_settings,
            absent=CheckResult(
                "settings.SMTP", CheckStatus.SKIPPED, "SMTP: Not configured (optional)"
            ),
        )
    )
    results.append(
        _settings_result(
            config,
            label="Console",
            keys=("consoleapi", "general"),
            reader=config.get_console_api_settings,
            absent=CheckResult(
                "consoleapi.general", CheckStatus.SKIPPED, "Console: Not configured (optional)"
            ),
            hint=lambda: _refresh_token_hint(
                config.settings.get("consoleapi", {}).get("general"),
                config.settings.get("users", {}),
                None,
                "consoleapi.toml",
            ),
        )
    )
    if config.get_licensing_settings():
        results.append(CheckResult("licensing", CheckStatus.OK, "Licensing"))
    else:
        results.append(
            CheckResult("licensing", CheckStatus.SKIPPED, "Licensing: Not configured (optional)")
        )
    return results


def check_scope_settings(config: Config, scope: str) -> list[CheckResult]:
    """Validate a scope's ``monitoring.toml`` and Console account.

    Args:
        config: Config instance to check.
        scope: A known scope name.
    """
    scope_tree = config.get_scope_settings(scope)
    if scope_tree.get("monitoring"):
        monitoring = CheckResult("monitoring", CheckStatus.OK, "Monitoring")
    else:
        monitoring = CheckResult(
            "monitoring", CheckStatus.SKIPPED, "Monitoring: Not configured (optional)"
        )
    console = _settings_result(
        config,
        label="Console",
        keys=("consoleapi", "general"),
        reader=lambda: config.get_console_api_settings(scope=scope),
        absent=CheckResult(
            "consoleapi.general", CheckStatus.SKIPPED, "Console: Not configured (optional)"
        ),
        tree=scope_tree,
        error_prefix=f"{scope}/",
        hint=lambda: _refresh_token_hint(
            scope_tree.get("consoleapi", {}).get("general"),
            scope_tree.get("users", {}),
            scope,
            f"{scope}/consoleapi.toml",
        ),
    )
    return [monitoring, console]


def check_cluster_credentials(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Check that every cluster resolves credentials.

    Args:
        config: Config instance to check.
        scope: Check only this scope's clusters; None checks every cluster.
    """
    results: list[CheckResult] = []
    for name in _in_scope(config, "clusters", scope):
        subject = f"clusters.{name}.credentials"
        try:
            user, _enc = config.get_user("clusters", name)
        except ConfigurationError:
            results.append(
                CheckResult(
                    subject,
                    CheckStatus.ERROR,
                    f"{name}: Missing credentials",
                    (f"Cluster '{name}' has no credentials configured",),
                    f"Set them with: nf config set-credential --cluster {name} --user USER",
                )
            )
        else:
            results.append(CheckResult(subject, CheckStatus.OK, f"{name}: {user}"))
    return results


def check_aiqums(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Validate the ``[aiqums]`` entries; each needs an ``ip``."""
    return _check_entries(
        "aiqums", AIQUMConfig, _in_scope(config, "aiqums", scope), require_ip=True
    )


def check_aiqum_credentials(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Check that every AIQUM resolves credentials (decrypting a SOPS value locally)."""
    results: list[CheckResult] = []
    for name in _in_scope(config, "aiqums", scope):
        subject = f"aiqums.{name}.credentials"
        try:
            user, _enc = config.get_user("aiqums", name)
        except ConfigurationError:
            results.append(
                CheckResult(
                    subject,
                    CheckStatus.ERROR,
                    f"{name}: Missing credentials",
                    (f"AIQUM '{name}' has no credentials configured",),
                    "Set them with: nf config set-credential --type aiqums "
                    f"--name {name} --user USER",
                )
            )
        else:
            results.append(CheckResult(subject, CheckStatus.OK, f"{name}: {user}"))
    return results


def check_connectors(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Validate the ``[connectors]`` entries."""
    return _check_entries("connectors", ConnectorConfig, _in_scope(config, "connectors", scope))


def check_cloudinsights(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Validate the ``[cloudinsights]`` tenant entries."""
    return _check_entries(
        "cloudinsights", CloudInsightsConfig, _in_scope(config, "cloudinsights", scope)
    )


def check_cloudinsights_credentials(config: Config, scope: str | None = None) -> list[CheckResult]:
    """Check that every tenant resolves a base URL and API token.

    The token is read to prove it is present and never leaves this function; the
    failure reason is not reported, as it could quote the configuration.
    """
    results: list[CheckResult] = []
    for name in _in_scope(config, "cloudinsights", scope):
        subject = f"cloudinsights.{name}.credentials"
        try:
            config.get_dii_api_settings(name)
        except ConfigurationError:
            results.append(
                CheckResult(
                    subject,
                    CheckStatus.ERROR,
                    f"{name}: Missing API token or base_url",
                    (f"Cloud Insights '{name}' has no API token or base_url configured",),
                    "Store the token with: nf config set-credential --type cloudinsights "
                    f"--name {name} --user token. Set base_url on the tenant or in "
                    "<config>/apis/dii/diiapi.toml.",
                )
            )
        else:
            results.append(CheckResult(subject, CheckStatus.OK, f"{name}: API token"))
    return results


def configured_apis(config: Config) -> set[str]:
    """Return the APIs in use, judged from the loaded TOML only (no decryption)."""

    def has_general(settings: dict[str, Any], key: str) -> bool:
        section = settings.get(key)
        return isinstance(section, dict) and "general" in section

    apis: set[str] = set()
    if has_general(config.settings, "ontapapi"):
        apis.add("ontap")
    if has_general(config.settings, "aiqumapi"):
        apis.add("aiqum")
    if has_general(config.settings, "diiapi") or config.data.get("cloudinsights"):
        apis.add("dii")
    if has_general(config.settings, "consoleapi") or any(
        has_general(tree, "consoleapi") for tree in config.scope_settings.values()
    ):
        apis.add("console")
    return apis


def spec_download_hint(api: str) -> str:
    """Return the fix hint of a missing spec: the command that downloads it.

    The hint also names the repository file, for copying it by hand.
    """
    source = next((src for _, name, _, src in SPEC_FILES if name == api), "the spec file")
    return (
        f"Run: nf config download-spec --api {api} (downloads {source} at the installed "
        f"release, {__version__}); see {CONFIGURATION_DOC} (Spec files)."
    )


def check_spec_files(config: Config) -> list[CheckResult]:
    """Check that the OpenAPI spec of every configured API is in ``<config>/apis/``.

    A missing spec is a warning: the client raises ``FileNotFoundError`` when it is
    built, but nothing is wrong with the configuration itself.
    """
    configured = configured_apis(config)
    results: list[CheckResult] = []
    for display, api, file_name, _source in SPEC_FILES:
        if api not in configured:
            continue
        path = config.get_schema_location(api) / file_name
        subject = f"spec.{api}"
        if path.is_file():
            results.append(CheckResult(subject, CheckStatus.OK, f"{display} spec"))
        else:
            results.append(
                CheckResult(
                    subject,
                    CheckStatus.WARNING,
                    f"{display} spec: missing {path}",
                    hint=spec_download_hint(api),
                )
            )
    return results


def run_static_checks(config: Config, scope: str | None = None) -> list[CheckSection]:
    """Run every static check, in display order.

    The first four sections are always present, even when empty. Later sections
    appear only when they have results. With ``scope`` the inventory checks cover
    that scope's objects and the spec files are not checked.

    Args:
        config: Config instance to check.
        scope: A known scope name, or None for the root.

    Raises:
        ConfigurationError: If ``scope`` is not a known scope.
    """
    if scope is None:
        users = config.settings.get("users", {})
        users_results = check_users(users)
        settings_title = "Settings"
        settings_results = check_settings(config)
    else:
        users = config.get_scope_settings(scope).get("users", {})
        users_results = check_users(users, label_prefix=f"{scope}/users", scope=scope)
        settings_title = f"Scope settings ({scope})"
        settings_results = check_scope_settings(config, scope)

    optional = [
        ("AIQUM", check_aiqums(config, scope)),
        ("AIQUM Credentials", check_aiqum_credentials(config, scope)),
        ("Connectors", check_connectors(config, scope)),
        ("Cloud Insights", check_cloudinsights(config, scope)),
        ("Cloud Insights Credentials", check_cloudinsights_credentials(config, scope)),
        ("Spec Files", check_spec_files(config) if scope is None else []),
    ]
    sections = [
        CheckSection("Clusters", tuple(check_clusters(config, scope))),
        CheckSection("Users", tuple(users_results)),
        CheckSection(settings_title, tuple(settings_results)),
        CheckSection("Cluster Credentials", tuple(check_cluster_credentials(config, scope))),
    ]
    sections.extend(CheckSection(title, tuple(rows)) for title, rows in optional if rows)
    return sections
