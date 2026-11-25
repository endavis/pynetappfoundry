"""Offline environment checks for ``nf doctor``: SOPS, the age key, the caches and the
config-to-Console cluster name comparison.

No check here makes a network call, prints a value, or puts a ciphertext, a plaintext
or a SOPS error message in a result. A SOPS failure is reported by its class name
only. The caches are opened read-only through a ``mode=ro`` URI, so a check never
creates, migrates or modifies a cache file. See ADR-0035.
"""

from __future__ import annotations

import os
import shlex
import sqlite3
from collections.abc import Collection, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pynetappfoundry.core.config import (
    SOPS_SETTING_TARGETS,
    VALID_DATA_TYPES,
    Config,
    ConfigurationError,
)
from pynetappfoundry.core.config_checks import (
    CONFIGURATION_DOC,
    CheckResult,
    CheckSection,
    CheckStatus,
)
from pynetappfoundry.doctor import API_NAMES
from pynetappfoundry.doctor.selection import DATA_TYPE_APIS, SETTINGS_APIS, USER_TYPE_APIS

CACHE_STALE_DAYS = 30
"""Age in days after which a cache is reported stale (the ``nf cache status`` default)."""

_MAX_LISTED = 5


# --- SOPS ---------------------------------------------------------------------------


def _walk_encrypted(value: Any, subject: str, found: dict[str, str]) -> None:
    """Collect the SOPS-encrypted strings under ``value``, keyed by dotted subject."""
    from pynetappfoundry.utils.sops import is_encrypted

    if isinstance(value, str):
        if is_encrypted(value):
            found[subject] = value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            _walk_encrypted(item, f"{subject}.{key}", found)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _walk_encrypted(item, f"{subject}[{index}]", found)


def _walk_settings(
    tree: Any, prefix: str, found: dict[str, str], apis: Collection[str] | None
) -> None:
    """Collect SOPS values in a settings tree, keeping only the stems of ``apis``."""
    if apis is None or not isinstance(tree, Mapping):
        _walk_encrypted(tree, prefix, found)
        return
    for stem, value in tree.items():
        if stem == "users":
            if not isinstance(value, Mapping):
                continue
            for utype, accounts in value.items():
                if USER_TYPE_APIS.get(utype) in apis:
                    _walk_encrypted(accounts, f"{prefix}.users.{utype}", found)
        elif SETTINGS_APIS.get(stem) in apis:
            _walk_encrypted(value, f"{prefix}.{stem}", found)


def find_sops_values(
    config: Config,
    scope: str | None = None,
    *,
    apis: Collection[str] | None = None,
) -> dict[str, str]:
    """Find every SOPS value the configuration holds.

    Args:
        config: Loaded configuration.
        scope: Only the settings of this scope and the data objects in it; None
            walks the root settings, every scope's settings and every data object.
        apis: Only the values that belong to these APIs (settings stems, user
            types and data types they read); None keeps every value.

    Returns:
        Dotted subject (such as ``settings.users.clusters.enc``) to ciphertext. The
        ciphertext is for decrypting; callers must never put it in a result.
    """
    found: dict[str, str] = {}
    if scope is None:
        _walk_settings(config.settings, "settings", found, apis)
        for name, tree in config.scope_settings.items():
            _walk_settings(tree, f"scope.{name}", found, apis)
    else:
        _walk_settings(config.scope_settings.get(scope, {}), f"scope.{scope}", found, apis)
    for data_type, objects in config.data.items():
        if apis is not None and DATA_TYPE_APIS.get(data_type) not in apis:
            continue
        for name, entry in objects.items():
            if scope is None or config.get_scope(data_type, name) == scope:
                _walk_encrypted(entry, f"{data_type}.{name}", found)
    return found


def _is_plaintext(value: Any) -> bool:
    """Return True for a non-blank string that is not a ``SOPS[...]`` value."""
    from pynetappfoundry.utils.sops import is_encrypted

    return isinstance(value, str) and bool(value.strip()) and not is_encrypted(value)


def _set_credential(*args: str, user: Any = None, with_user: bool = True) -> str:
    """Build a ``nf config set-credential`` command.

    ``with_user`` False omits ``--user``; otherwise a blank or non-string ``user``
    becomes the literal ``<user>`` placeholder.
    """
    parts = ["nf", "config", "set-credential", *(shlex.quote(a) for a in args)]
    if with_user:
        shown = shlex.quote(user) if isinstance(user, str) and user.strip() else "<user>"
        parts += ["--user", shown]
    return " ".join(parts)


def _walk_plaintext_settings(
    tree: Any,
    prefix: str,
    found: dict[str, str],
    apis: Collection[str] | None,
    scope: str | None,
) -> None:
    """Collect plaintext secret fields in one settings tree (root or a scope's)."""
    if not isinstance(tree, Mapping):
        return
    for target, (stem, table, key) in SOPS_SETTING_TARGETS.items():
        # A scope only overrides consoleapi among the settings that hold secrets.
        if scope is not None and stem != "consoleapi":
            continue
        if apis is not None and SETTINGS_APIS.get(stem) not in apis:
            continue
        section = tree.get(stem)
        general = section.get(table) if isinstance(section, Mapping) else None
        if isinstance(general, Mapping) and _is_plaintext(general.get(key)):
            args = ["--setting", target] + (["--scope", scope] if scope else [])
            found[f"{prefix}.{stem}.{table}.{key}"] = _set_credential(*args, with_user=False)
    users = tree.get("users")
    if not isinstance(users, Mapping):
        return
    for utype in sorted(VALID_DATA_TYPES | {"console"}):
        account = users.get(utype)
        if not isinstance(account, Mapping):
            continue
        if apis is not None and USER_TYPE_APIS.get(utype) not in apis:
            continue
        if _is_plaintext(account.get("enc")):
            args = ["--type", utype] + (["--scope", scope] if scope else [])
            found[f"{prefix}.users.{utype}.enc"] = _set_credential(*args, user=account.get("user"))


def find_plaintext_secrets(
    config: Config,
    scope: str | None = None,
    *,
    apis: Collection[str] | None = None,
) -> dict[str, str]:
    """Find the known secret fields that hold a plaintext value.

    Only the fields ``nf config set-credential`` can encrypt are checked, so a
    plain ``user`` or ``ip`` is never reported. The arguments match
    ``find_sops_values``.

    Returns:
        Dotted subject (the same names ``find_sops_values`` uses) to the
        ``set-credential`` command that stores it encrypted. The value itself is
        never returned.
    """
    found: dict[str, str] = {}
    if scope is None:
        _walk_plaintext_settings(config.settings, "settings", found, apis, None)
        for name, tree in config.scope_settings.items():
            _walk_plaintext_settings(tree, f"scope.{name}", found, apis, name)
    else:
        _walk_plaintext_settings(
            config.scope_settings.get(scope, {}), f"scope.{scope}", found, apis, scope
        )
    for data_type, objects in config.data.items():
        if apis is not None and DATA_TYPE_APIS.get(data_type) not in apis:
            continue
        for name, entry in objects.items():
            if scope is not None and config.get_scope(data_type, name) != scope:
                continue
            if _is_plaintext(entry.get("enc")):
                if data_type == "clusters":
                    command = _set_credential("--cluster", name, user=entry.get("user"))
                else:
                    command = _set_credential(
                        "--type", data_type, "--name", name, user=entry.get("user")
                    )
                found[f"{data_type}.{name}.enc"] = command
            if data_type == "cloudinsights" and _is_plaintext(entry.get("rw_enc")):
                found[f"{data_type}.{name}.rw_enc"] = _set_credential(
                    "--type", data_type, "--name", name, "--read-write", with_user=False
                )
    return found


def _age_key_location() -> tuple[bool, str]:
    """Return ``(present, description)`` of the age key, without reading it."""
    from pynetappfoundry.utils.sops import get_age_key_path

    if os.environ.get("SOPS_AGE_KEY"):
        return True, "SOPS_AGE_KEY is set"
    path = get_age_key_path()
    return path.is_file(), f"key file {path}"


def check_sops(
    config: Config,
    scope: str | None = None,
    *,
    apis: Collection[str] | None = None,
) -> list[CheckResult]:
    """Check ``sops``, the age key, that every SOPS value decrypts and no secret is plaintext.

    A known secret field holding a plaintext value is a WARNING row naming the
    ``set-credential`` command that encrypts it; it never contains the value.

    Args:
        config: Loaded configuration.
        scope: Limit the values checked to this scope's.
        apis: Limit the values checked to these APIs'. When none of them has a
            SOPS or plaintext secret value, return no rows at all; None checks every
            value.
    """
    from pynetappfoundry.utils.sops import SOPSError, decrypt_value, is_sops_installed

    values = find_sops_values(config, scope, apis=apis)
    plaintext = find_plaintext_secrets(config, scope, apis=apis)
    if apis is not None and not values and not plaintext:
        return []
    plaintext_rows = [
        CheckResult(
            f"sops.{subject}",
            CheckStatus.WARNING,
            f"{subject}: plaintext (not SOPS-encrypted)",
            hint=f"Store it encrypted with: {command}",
        )
        for subject, command in plaintext.items()
    ]
    installed = is_sops_installed()
    results: list[CheckResult] = []

    if installed:
        results.append(CheckResult("env.sops", CheckStatus.OK, "sops is installed"))
    elif values:
        results.append(
            CheckResult(
                "env.sops",
                CheckStatus.ERROR,
                "sops is not installed",
                ("sops is not on PATH, but the configuration has SOPS values",),
                f"Install sops and age; see {CONFIGURATION_DOC}.",
            )
        )
    else:
        results.append(
            CheckResult(
                "env.sops",
                CheckStatus.SKIPPED,
                "sops: not installed (optional)",
                hint="To encrypt credentials, install sops and run: nf config init-sops",
            )
        )

    present, where = _age_key_location()
    key_hint = "Create or point to your age key with: nf config init-sops"
    if not os.environ.get("SOPS_AGE_KEY_FILE"):
        key_hint += " (it writes SOPS_AGE_KEY_FILE to .envrc.local)"
    if present:
        results.append(CheckResult("env.age_key", CheckStatus.OK, f"age key: {where}"))
    elif values:
        results.append(
            CheckResult(
                "env.age_key",
                CheckStatus.ERROR,
                f"age key missing: {where}",
                (f"No age key found ({where}), but the configuration has SOPS values",),
                key_hint,
            )
        )
    else:
        results.append(
            CheckResult(
                "env.age_key",
                CheckStatus.SKIPPED,
                f"age key: not found ({where}; optional)",
                hint=key_hint,
            )
        )

    if not values:
        results.append(
            CheckResult("sops.values", CheckStatus.SKIPPED, "No SOPS values in the configuration")
        )
        return results + plaintext_rows
    if not installed:
        return results + plaintext_rows
    for subject, ciphertext in values.items():
        try:
            decrypt_value(ciphertext)
        except SOPSError as e:
            label = f"{subject}: SOPS value does not decrypt ({type(e).__name__})"
            results.append(
                CheckResult(
                    f"sops.{subject}",
                    CheckStatus.ERROR,
                    label,
                    (label,),
                    "Check that SOPS_AGE_KEY_FILE points to the key that encrypted it, "
                    "or store the value again with: nf config set-credential",
                )
            )
        else:
            results.append(CheckResult(f"sops.{subject}", CheckStatus.OK, f"{subject}: decrypts"))
    return results + plaintext_rows


# --- Caches -------------------------------------------------------------------------


def _parse_time(text: str) -> datetime | None:
    """Parse a cached timestamp (``Z``, offset or naive-as-UTC); None if unparsable."""
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _schema_version(conn: sqlite3.Connection) -> int:
    """Return the schema version as ``SQLiteDB._get_schema_version`` does."""
    has_version = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='_schema_version'"
    ).fetchone()
    if has_version is None:
        has_tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' AND name != '_schema_version'"
        ).fetchone()
        return 1 if has_tables is not None else 0
    row = conn.execute("SELECT version FROM _schema_version").fetchone()
    return 1 if row is None else int(row[0])


def _read_cache(
    path: Path, table: str, name_column: str | None
) -> tuple[int, int, str | None, str | None, set[str]]:
    """Read ``(version, rows, oldest, newest, names)`` from a cache without writing."""
    conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        version = _schema_version(conn)
        has_table = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
        if has_table is None:
            return version, 0, None, None, set()
        # ``table`` and ``name_column`` are module constants, never caller text.
        count, oldest, newest = conn.execute(
            f"SELECT COUNT(*), MIN(cached_at), MAX(cached_at) FROM {table}"  # constant table name
        ).fetchone()
        names: set[str] = set()
        if name_column is not None:
            names = {
                str(r[0])
                for r in conn.execute(f"SELECT {name_column} FROM {table}")  # constant names
            }
        return version, int(count), oldest, newest, names
    finally:
        conn.close()


def _check_one_cache(
    *,
    subject: str,
    title: str,
    path: Path,
    expected_version: int,
    table: str,
    name_column: str | None,
    refresh: str,
    ttl_days: int,
    expected_names: set[str] | None = None,
) -> list[CheckResult]:
    """Check one cache file and return its rows."""
    if not path.is_file():
        return [
            CheckResult(
                subject,
                CheckStatus.WARNING,
                f"{title}: not found ({path})",
                hint=f"Build it with: {refresh}",
            )
        ]
    try:
        version, rows, oldest, _newest, names = _read_cache(path, table, name_column)
    except sqlite3.DatabaseError as e:
        label = f"{title}: cannot read {path} ({type(e).__name__})"
        return [
            CheckResult(
                subject,
                CheckStatus.ERROR,
                label,
                (label,),
                f"Delete and rebuild it with: nf cache clear, then {refresh}",
            )
        ]

    if version > expected_version:
        label = f"{title}: schema v{version} is newer than this release (v{expected_version})"
        return [
            CheckResult(
                subject,
                CheckStatus.ERROR,
                label,
                (f"{label}; downgrade is unsupported (ADR-0018)",),
                f"Upgrade pynetappfoundry, or run nf cache clear and then: {refresh}",
            )
        ]

    results: list[CheckResult] = []
    if version < expected_version and version > 0:
        results.append(
            CheckResult(
                subject,
                CheckStatus.WARNING,
                f"{title}: schema v{version}, this release uses v{expected_version}",
                hint=f"It upgrades on the next cache command; then run: {refresh}",
            )
        )
    if rows == 0:
        results.append(
            CheckResult(
                subject,
                CheckStatus.WARNING,
                f"{title}: empty ({path})",
                hint=f"Fill it with: {refresh}",
            )
        )
        return results

    when = _parse_time(oldest) if oldest else None
    if when is None:
        age_label = "oldest entry has no readable time"
        stale = False
    else:
        days = (datetime.now(UTC) - when).days
        age_label = f"oldest entry {days} day(s) old"
        stale = days > ttl_days
    if stale:
        results.append(
            CheckResult(
                subject,
                CheckStatus.WARNING,
                f"{title}: {age_label}, past {ttl_days} days",
                hint=f"Refresh it with: {refresh}",
            )
        )
    if expected_names is not None:
        missing = sorted(expected_names - names)
        if missing:
            listed = ", ".join(missing[:_MAX_LISTED])
            more = f" and {len(missing) - _MAX_LISTED} more" if len(missing) > _MAX_LISTED else ""
            results.append(
                CheckResult(
                    f"{subject}.coverage",
                    CheckStatus.WARNING,
                    f"{title}: not cached: {listed}{more}",
                    hint=f"Cache them with: {refresh}",
                )
            )
    if not results:
        results.append(
            CheckResult(
                subject, CheckStatus.OK, f"{title}: v{version}, {rows} entries, {age_label}"
            )
        )
    return results


def check_caches(
    config: Config,
    apis: tuple[str, ...],
    clusters: dict[str, Any],
    *,
    ttl_days: int = CACHE_STALE_DAYS,
) -> list[CheckResult]:
    """Check each cache the selected APIs use, by presence, schema version and age.

    Args:
        config: Loaded configuration.
        apis: The selected APIs (``ontap`` -> ONTAP cache, ``aiqum`` -> AIQUM cache,
            ``console`` -> OCCM cache).
        clusters: The configured (filtered, scoped) clusters the ONTAP cache should hold.
        ttl_days: Age of the oldest entry after which a cache is stale.
    """
    results: list[CheckResult] = []
    if "ontap" in apis and clusters:
        from pynetappfoundry.cache.db import ClusterMetadataDB

        results.extend(
            _check_one_cache(
                subject="cache.ontap",
                title="ONTAP cache",
                path=ClusterMetadataDB.default_path(config),
                expected_version=ClusterMetadataDB.SCHEMA_VERSION,
                table="cluster_metadata",
                name_column="cluster_name",
                refresh="nf cache refresh --all",
                ttl_days=ttl_days,
                expected_names=set(clusters),
            )
        )
    if "aiqum" in apis and config.data.get("aiqums"):
        from pynetappfoundry.cache.aiqum_db import AiqumCacheDB

        results.extend(
            _check_one_cache(
                subject="cache.aiqum",
                title="AIQUM cache",
                path=AiqumCacheDB.default_path(config),
                expected_version=AiqumCacheDB.SCHEMA_VERSION,
                table="aiqum_collections",
                name_column=None,
                refresh="nf cache aiqum refresh --all",
                ttl_days=ttl_days,
            )
        )
    if "console" in apis:
        try:
            accounts = config.console_account_scopes()
        except ConfigurationError as e:
            label = f"OCCM cache: Console account not resolvable: {e}"
            results.append(
                CheckResult(
                    "cache.occm",
                    CheckStatus.ERROR,
                    label,
                    (label,),
                    "Fix the Console refresh token; see nf config validate.",
                )
            )
            accounts = []
        if accounts:
            from pynetappfoundry.cache.occm_db import OccmCacheDB

            results.extend(
                _check_one_cache(
                    subject="cache.occm",
                    title="OCCM cache",
                    path=OccmCacheDB.default_path(config),
                    expected_version=OccmCacheDB.SCHEMA_VERSION,
                    table="occm_collections",
                    name_column=None,
                    refresh="nf cache occm refresh",
                    ttl_days=ttl_days,
                )
            )
    return results


def run_environment_checks(
    config: Config,
    *,
    scope: str | None,
    apis: tuple[str, ...] = API_NAMES,
    sops_apis: Collection[str] | None = None,
    clusters: dict[str, Any],
    cluster_filter_active: bool = False,
) -> list[CheckSection]:
    """Run the offline environment checks; a section appears only when it has rows.

    ``apis`` selects the caches; ``sops_apis`` limits the SOPS checks (None: all).
    """
    sections = [
        CheckSection("SOPS", tuple(check_sops(config, scope, apis=sops_apis))),
        CheckSection("Caches", tuple(check_caches(config, apis, clusters))),
    ]
    if "console" in apis or "ontap" in apis:
        from pynetappfoundry.doctor.console_clusters import check_console_clusters

        sections.append(
            CheckSection(
                "Console clusters",
                tuple(
                    check_console_clusters(
                        config,
                        clusters,
                        scope=scope,
                        cluster_filter_active=cluster_filter_active,
                    )
                ),
            )
        )
    return [section for section in sections if section.results]
