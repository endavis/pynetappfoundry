"""Offline ``nf doctor`` check: config ``[clusters]`` against Console working environments.

A ``[clusters.NAME]`` key must equal the cluster's real name, which is Console's
``ontapClusterProperties.clusterName`` (ADR-0035). A record Console gives no cluster
name (seen on some Azure working environments) falls back to the working environment
name, ``name``, for the name match only. The check reads the OCCM and ONTAP
caches only, through ``mode=ro`` URIs, so it never creates, migrates or writes a cache
file and makes no network call. It compares per Console account. It imports neither
Rich nor click.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.occm_collector import OCCM_WORKING_ENVIRONMENT_MAPPINGS
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.config_checks import CheckResult, CheckStatus
from pynetappfoundry.doctor.environment import (
    _MAX_LISTED,
    CACHE_STALE_DAYS,
    _parse_time,
    _schema_version,
)

_SUBJECT = "console_clusters"


@dataclass(frozen=True)
class ConsoleCluster:
    """One ONTAP working environment as the OCCM cache keeps it."""

    account: str | None
    public_id: str | None
    name: str | None
    display: str
    uuid: str | None
    ips: frozenset[str]
    environment_name: str | None = None


def _text(value: Any) -> str | None:
    """Return ``value`` stripped when it is a non-empty string, else None."""
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _lif_ips(lifs: Any) -> set[str]:
    """Collect the ``ip`` of every dict entry in a LIF list, ignoring anything else."""
    found: set[str] = set()
    if isinstance(lifs, list):
        for lif in lifs:
            if isinstance(lif, dict) and (ip := _text(lif.get("ip"))):
                found.add(ip)
    return found


def cluster_from_record(record: Mapping[str, Any], account: str | None) -> ConsoleCluster:
    """Extract name, UUID and every management IP from one raw working-environment record."""
    props = record.get("ontapClusterProperties")
    props = props if isinstance(props, dict) else {}
    name = _text(props.get("clusterName"))
    public_id = _text(record.get("publicId"))
    ips: set[str] = set()
    if address := _text(props.get("clusterAddress")):
        ips.add(address)
    ips |= _lif_ips(props.get("lifs"))
    nodes = props.get("nodes")
    if isinstance(nodes, list):
        for node in nodes:
            if isinstance(node, dict):
                ips |= _lif_ips(node.get("lifs"))
    cluster_props = record.get("clusterProperties")
    if isinstance(cluster_props, dict):
        ips |= _lif_ips(cluster_props.get("lifs"))
    environment_name = _text(record.get("name"))
    display = name or environment_name or public_id or "(unnamed)"
    return ConsoleCluster(
        account=account,
        public_id=public_id,
        name=name,
        display=display,
        uuid=_text(props.get("clusterUuid")),
        ips=frozenset(ips),
        environment_name=environment_name,
    )


def read_occm_clusters(
    path: Path,
) -> tuple[int, dict[str | None, list[ConsoleCluster]], dict[str | None, str | None]]:
    """Read ``(schema version, clusters per account, oldest cached_at per account)``.

    Opens the cache read-only. Working environments are deduplicated per account by
    ``publicId``, because HA agents list the same one twice.
    """
    marks = ", ".join("?" for _ in OCCM_WORKING_ENVIRONMENT_MAPPINGS)
    conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        version = _schema_version(conn)
        has_tables = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' "
            "AND name IN ('occm_collections', 'occm_records')"
        ).fetchone()[0]
        if has_tables < 2:
            return version, {}, {}
        oldest: dict[str | None, str | None] = {
            row[0]: row[1]
            for row in conn.execute(
                f"SELECT scope, MIN(cached_at) FROM occm_collections "  # constant marks
                f"WHERE mapping IN ({marks}) GROUP BY scope",
                OCCM_WORKING_ENVIRONMENT_MAPPINGS,
            )
        }
        rows = conn.execute(
            "SELECT c.scope, r.record FROM occm_records r "  # constant marks
            "JOIN (SELECT DISTINCT agent_id, scope FROM occm_collections) c "
            "USING (agent_id) "
            f"WHERE r.mapping IN ({marks}) ORDER BY r._row_id",
            OCCM_WORKING_ENVIRONMENT_MAPPINGS,
        ).fetchall()
    finally:
        conn.close()

    clusters: dict[str | None, list[ConsoleCluster]] = {}
    seen: set[tuple[str | None, str]] = set()
    for scope, text in rows:
        try:
            record = json.loads(text)
        except ValueError:
            continue
        if not isinstance(record, dict):
            continue
        cluster = cluster_from_record(record, scope)
        if cluster.public_id is not None:
            marker = (scope, cluster.public_id)
            if marker in seen:
                continue
            seen.add(marker)
        clusters.setdefault(scope, []).append(cluster)
    return version, clusters, oldest


def read_ontap_uuids(path: Path) -> dict[str, str]:
    """Return ``{config cluster key: UUID}`` from the ONTAP cache; ``{}`` when unreadable."""
    if not path.is_file():
        return {}
    try:
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            return {
                str(key): str(uuid)
                for key, uuid in conn.execute(
                    "SELECT cluster_name, uuid FROM ontapcluster WHERE uuid IS NOT NULL"
                )
            }
        finally:
            conn.close()
    except sqlite3.DatabaseError:
        return {}


def _listed(items: Sequence[str]) -> str:
    """Join up to ``_MAX_LISTED`` items and say how many more there are."""
    shown = ", ".join(items[:_MAX_LISTED])
    extra = len(items) - _MAX_LISTED
    return f"{shown} and {extra} more" if extra > 0 else shown


def match_account(
    account: str | None,
    entries: Mapping[str, str | None],
    uuids: Mapping[str, str],
    console: Sequence[ConsoleCluster],
    *,
    report_console_only: bool,
) -> list[CheckResult]:
    """Compare one account's config entries (key to ip) with its Console clusters.

    A key matches by name when it equals the cluster name, or the working environment name
    of a record that has no cluster name.
    """
    shown = account or "root"
    base = f"{_SUBJECT}.{shown}"
    remaining = sorted(console, key=lambda c: c.display)
    unmatched: list[str] = []
    name_matches = 0
    fallback_matches = 0

    for key in sorted(entries):
        hit = next((c for c in remaining if c.name == key), None)
        if hit is None:
            hit = next((c for c in remaining if c.name is None and c.environment_name == key), None)
            if hit is not None:
                fallback_matches += 1
        if hit is None:
            unmatched.append(key)
        else:
            remaining.remove(hit)
            name_matches += 1

    results: list[CheckResult] = []
    found: dict[str, tuple[ConsoleCluster, str]] = {}
    for key in list(unmatched):  # pass 1: UUID
        uuid = uuids.get(key)
        hit = next((c for c in remaining if uuid and c.uuid == uuid), None)
        if hit is not None:
            remaining.remove(hit)
            found[key] = (hit, "UUID")
    for key in list(unmatched):  # pass 2: IP
        ip = (entries[key] or "").strip()
        if key in found or not ip:
            continue
        hit = next((c for c in remaining if ip in c.ips), None)
        if hit is not None:
            remaining.remove(hit)
            found[key] = (hit, "IP")

    for key in sorted(found):
        cluster, how = found[key]
        label = f"{shown}: [clusters] key {key}: Console calls this cluster {cluster.display}"
        label += f" (matched by {how})"
        hint = (
            f"Rename the [clusters] key {key} to {cluster.name}"
            if cluster.name
            else f"Console has no cluster name for {cluster.display}; check it in Console"
        )
        results.append(CheckResult(f"{base}.{key}", CheckStatus.ERROR, label, (label,), hint))
    unmatched = [k for k in unmatched if k not in found]

    if unmatched:
        results.append(
            CheckResult(
                f"{base}.config_only",
                CheckStatus.WARNING,
                f"{shown}: in your config, not found in Console: {_listed(unmatched)}",
                hint="Check the spelling, or refresh the cache with: nf cache occm refresh",
            )
        )
    if remaining and report_console_only:
        results.append(
            CheckResult(
                f"{base}.console_only",
                CheckStatus.WARNING,
                f"{shown}: in Console, not in your config: "
                f"{_listed([c.display for c in remaining])}",
                hint="Add them to [clusters] in an inventory file, or ignore them",
            )
        )
    if name_matches or not results:
        label = f"{shown}: {name_matches} cluster(s) match Console by name"
        if fallback_matches:
            label += (
                f" ({fallback_matches} by working environment name; "
                "Console reports no cluster name for them)"
            )
        results.append(CheckResult(base, CheckStatus.OK, label))
    return results


def _refresh_command(account: str | None) -> str:
    return (
        "nf cache occm refresh" if account is None else f"nf cache occm refresh --scope {account}"
    )


def check_console_clusters(
    config: Config,
    clusters: Mapping[str, Any],
    *,
    scope: str | None,
    cluster_filter_active: bool,
    ttl_days: int = CACHE_STALE_DAYS,
) -> list[CheckResult]:
    """Compare the config clusters with Console's working environments, per account."""
    try:
        accounts = config.console_account_scopes()
    except ConfigurationError:
        return [
            CheckResult(
                _SUBJECT,
                CheckStatus.SKIPPED,
                "Console accounts not resolvable; see nf config validate",
            )
        ]
    if scope is not None:
        accounts = [a for a in accounts if a == scope]
    if not accounts:
        return []

    path = OccmCacheDB.default_path(config)
    if not path.is_file():
        return [
            CheckResult(
                _SUBJECT,
                CheckStatus.WARNING,
                f"Console clusters not compared: OCCM cache not found ({path})",
                hint="Build it with: nf cache occm refresh",
            )
        ]
    try:
        version, console, oldest = read_occm_clusters(path)
    except sqlite3.DatabaseError as e:
        return [
            CheckResult(
                _SUBJECT,
                CheckStatus.WARNING,
                f"Console clusters not compared: cannot read the OCCM cache ({type(e).__name__})",
                hint="Delete and rebuild it with: nf cache clear, then nf cache occm refresh",
            )
        ]
    if version > OccmCacheDB.SCHEMA_VERSION:
        return [
            CheckResult(
                _SUBJECT,
                CheckStatus.WARNING,
                f"Console clusters not compared: OCCM cache schema v{version} is newer "
                f"than this release (v{OccmCacheDB.SCHEMA_VERSION})",
                hint="Upgrade pynetappfoundry, or run nf cache clear and then: "
                "nf cache occm refresh",
            )
        ]

    uuids = read_ontap_uuids(ClusterMetadataDB.default_path(config))
    results: list[CheckResult] = []
    for account in accounts:
        shown = account or "root"
        stamp = oldest.get(account)
        when = _parse_time(stamp) if stamp else None
        if stamp is None:
            reason = "no working environments cached"
        elif when is not None and (datetime.now(UTC) - when).days > ttl_days:
            reason = f"cache older than {ttl_days} days"
        else:
            reason = ""
        if reason:
            results.append(
                CheckResult(
                    f"{_SUBJECT}.{shown}",
                    CheckStatus.WARNING,
                    f"{shown}: not compared with Console: {reason}",
                    hint=f"Refresh it with: {_refresh_command(account)}",
                )
            )
            continue
        entries: dict[str, str | None] = {}
        for key, details in clusters.items():
            if config.get_scope("clusters", key) != account:
                continue
            ip = details.get("ip") if isinstance(details, Mapping) else None
            entries[key] = ip if isinstance(ip, str) else None
        results.extend(
            match_account(
                account,
                entries,
                uuids,
                console.get(account, []),
                report_console_only=not cluster_filter_active,
            )
        )
    return results
