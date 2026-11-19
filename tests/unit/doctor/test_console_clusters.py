"""Tests for the offline config-to-Console cluster name check (#1127)."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.occm_collector import OccmAgentSnapshot, OccmSnapshot
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.console.discovery import ConsoleInventory
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.config_checks import CheckResult, CheckStatus
from pynetappfoundry.doctor.console_clusters import (
    check_console_clusters,
    cluster_from_record,
)
from pynetappfoundry.doctor.environment import CACHE_STALE_DAYS, run_environment_checks
from pynetappfoundry.models.ontap.cluster.model import OntapCluster

DATA = '[settings]\ntype = "data"\n\n'
CONSOLE = {"consoleapi.toml": '[general]\nuser_token = "placeholder-token"\n'}
ORG1 = {
    "Org1/scope.toml": "",
    "Org1/consoleapi.toml": '[general]\nuser_token = "placeholder-token"\n',
}
ONPREM = "OccmOnpremWorkingEnvironment"
AWS_HA = "OccmAwsHaWorkingEnvironment"
U1 = "00000000-0000-0000-0000-000000000001"
U2 = "00000000-0000-0000-0000-000000000002"


@pytest.fixture(autouse=True)
def _isolate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SOPS_AGE_KEY", raising=False)
    monkeypatch.setenv("SOPS_AGE_KEY_FILE", str(tmp_path / "age-keys.txt"))


def _config(tmp_path: Path, files: dict[str, str]) -> Config:
    config_dir = tmp_path / "cfg"
    config_dir.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir=str(config_dir), script_name="test")


def _inv(**ips: str) -> str:
    return DATA + "".join(f'[clusters.{k}]\nip = "{v}"\n\n' for k, v in ips.items())


def _we(public_id: str, name: str | None, **props: Any) -> dict[str, Any]:
    ocp: dict[str, Any] = dict(props)
    if name is not None:
        ocp["clusterName"] = name
    return {"publicId": public_id, "name": f"we-{public_id}", "ontapClusterProperties": ocp}


def _make_occm(
    config: Config,
    agents: list[tuple[str, str | None, dict[str, list[dict[str, Any]]]]],
    *,
    age_days: int = 0,
) -> Path:
    path = OccmCacheDB.default_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC) - timedelta(days=age_days)
    snapshot = OccmSnapshot(
        cached_at=stamp,
        inventory=ConsoleInventory(),
        agents=tuple(
            OccmAgentSnapshot(
                agent_id=agent_id,
                scope=scope,
                organization_id="org-1",
                cached_at=stamp,
                records=records,
            )
            for agent_id, scope, records in agents
        ),
        failed_agents=(),
        skipped_agents=(),
    )
    with OccmCacheDB(db_path=path) as db:
        db.set(snapshot)
    return path


def _make_ontap(config: Config, uuids: dict[str, str]) -> None:
    path = ClusterMetadataDB.default_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    with ClusterMetadataDB(db_path=path) as db:
        for name, uuid in uuids.items():
            db.set(
                name,
                CachedClusterMetadata(
                    cluster_name=name,
                    cached_at=datetime.now(UTC),
                    cluster=OntapCluster(name=name, uuid=uuid),
                ),
            )


def _run(
    config: Config,
    *,
    scope: str | None = None,
    filtered: bool = False,
) -> dict[str, CheckResult]:
    clusters = config.get_clusters({})
    rows = check_console_clusters(config, clusters, scope=scope, cluster_filter_active=filtered)
    return {r.subject: r for r in rows}


def test_name_match_is_ok(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "c1")]})])

    rows = _run(config)

    assert set(rows) == {"console_clusters.root"}
    assert rows["console_clusters.root"].status is CheckStatus.OK
    assert "1 cluster(s)" in rows["console_clusters.root"].label


def test_uuid_match_reports_rename(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "prod-c1", clusterUuid=U1)]})])
    _make_ontap(config, {"c1": U1})

    rows = _run(config)

    row = rows["console_clusters.root.c1"]
    assert row.status is CheckStatus.ERROR
    assert "c1" in row.label
    assert "prod-c1" in row.label
    assert "UUID" in row.label
    assert row.hint is not None
    assert "Rename" in row.hint
    assert "console_clusters.root.console_only" not in rows


def test_ip_match_via_cluster_address(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "prod-c1", clusterAddress="192.0.2.1")]})])

    row = _run(config)["console_clusters.root.c1"]

    assert row.status is CheckStatus.ERROR
    assert "IP" in row.label


def test_aws_ha_node_lif_ip_match(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.21"), **CONSOLE})
    record = _we("w1", "cvo1", nodes=[{"lifs": [{"ip": "192.0.2.21", "privateIp": True}]}])
    _make_occm(config, [("a1", None, {AWS_HA: [record]})])

    row = _run(config)["console_clusters.root.c1"]

    assert row.status is CheckStatus.ERROR
    assert "cvo1" in row.label


def test_aws_ha_node_lif_ip_with_matching_name_is_ok(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(cvo1="192.0.2.21"), **CONSOLE})
    record = _we("w1", "cvo1", nodes=[{"lifs": [{"ip": "192.0.2.21"}]}])
    _make_occm(config, [("a1", None, {AWS_HA: [record]})])

    assert _run(config)["console_clusters.root"].status is CheckStatus.OK


def test_cluster_properties_lif_ip_match(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.30"), **CONSOLE})
    record = _we("w1", "cvo1")
    record["clusterProperties"] = {"lifs": [{"ip": "192.0.2.30"}]}
    _make_occm(config, [("a1", None, {AWS_HA: [record]})])

    assert _run(config)["console_clusters.root.c1"].status is CheckStatus.ERROR


def test_uuid_wins_over_ip(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(
        config,
        [
            (
                "a1",
                None,
                {
                    ONPREM: [
                        _we("w1", "by-ip", clusterAddress="192.0.2.1"),
                        _we("w2", "by-uuid", clusterUuid=U2),
                    ]
                },
            )
        ],
    )
    _make_ontap(config, {"c1": U2})

    rows = _run(config)

    assert "by-uuid" in rows["console_clusters.root.c1"].label
    assert "by-ip" in rows["console_clusters.root.console_only"].label


def test_name_matched_we_is_not_a_counterpart(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1", c2="192.0.2.1"), **CONSOLE})
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "c1", clusterAddress="192.0.2.1")]})])

    rows = _run(config)

    assert "console_clusters.root.c2" not in rows
    assert rows["console_clusters.root.config_only"].status is CheckStatus.WARNING
    assert "c2" in rows["console_clusters.root.config_only"].label


def test_leftovers_are_capped(tmp_path: Path) -> None:
    keys = {f"cfg{i}": f"192.0.2.{i + 1}" for i in range(7)}
    config = _config(tmp_path, {"inv.toml": _inv(**keys), **CONSOLE})
    wes = [_we(f"w{i}", f"con{i}") for i in range(8)]
    _make_occm(config, [("a1", None, {ONPREM: wes})])

    rows = _run(config)

    assert "and 2 more" in rows["console_clusters.root.config_only"].label
    assert "and 3 more" in rows["console_clusters.root.console_only"].label
    assert rows["console_clusters.root.console_only"].status is CheckStatus.WARNING


def test_filter_hides_console_only(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "c1"), _we("w2", "other")]})])

    assert "console_clusters.root.console_only" in _run(config)
    assert "console_clusters.root.console_only" not in _run(config, filtered=True)


def test_accounts_are_compared_separately(tmp_path: Path) -> None:
    files = {
        "inv.toml": _inv(c1="192.0.2.1"),
        "Org1/inv.toml": _inv(o1="192.0.2.9"),
        **CONSOLE,
        **ORG1,
    }
    config = _config(tmp_path, files)
    _make_occm(
        config,
        [
            ("a1", None, {ONPREM: [_we("w1", "c1")]}),
            ("a2", "Org1", {ONPREM: [_we("w2", "c1"), _we("w3", "o1")]}),
        ],
    )

    rows = _run(config)

    assert rows["console_clusters.root"].status is CheckStatus.OK
    assert rows["console_clusters.Org1"].status is CheckStatus.OK
    assert rows["console_clusters.Org1.console_only"].status is CheckStatus.WARNING
    assert "c1" in rows["console_clusters.Org1.console_only"].label
    assert "console_clusters.Org1.config_only" not in rows


def test_scope_without_account_gets_no_rows(tmp_path: Path) -> None:
    files = {
        "inv.toml": _inv(c1="192.0.2.1"),
        "Org1/scope.toml": "",
        "Org1/inv.toml": _inv(o1="192.0.2.9"),
        **CONSOLE,
    }
    config = _config(tmp_path, files)
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "c1")]})])

    assert set(_run(config)) == {"console_clusters.root"}


def test_scope_option_limits_accounts(tmp_path: Path) -> None:
    files = {
        "Org1/inv.toml": _inv(o1="192.0.2.9"),
        "inv.toml": _inv(c1="192.0.2.1"),
        **CONSOLE,
        **ORG1,
    }
    config = _config(tmp_path, files)
    _make_occm(
        config,
        [("a1", None, {ONPREM: [_we("w1", "c1")]}), ("a2", "Org1", {ONPREM: [_we("w2", "o1")]})],
    )
    clusters = {
        k: v
        for k, v in config.get_clusters({}).items()
        if config.get_scope("clusters", k) == "Org1"
    }

    rows = check_console_clusters(config, clusters, scope="Org1", cluster_filter_active=False)

    assert [r.subject for r in rows] == ["console_clusters.Org1"]


def test_missing_cache_warns_and_creates_nothing(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})

    rows = _run(config)

    assert rows["console_clusters"].status is CheckStatus.WARNING
    assert rows["console_clusters"].hint is not None
    assert "nf cache occm refresh" in rows["console_clusters"].hint
    assert not (tmp_path / "cfg" / ".cache").exists()


def test_stale_account_warns_with_scope_hint(tmp_path: Path) -> None:
    files = {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE, **ORG1}
    config = _config(tmp_path, files)
    _make_occm(config, [("a2", "Org1", {ONPREM: [_we("w2", "o1")]})], age_days=CACHE_STALE_DAYS + 5)

    rows = _run(config)

    assert (
        rows["console_clusters.Org1"].hint == "Refresh it with: nf cache occm refresh --scope Org1"
    )
    assert rows["console_clusters.root"].hint == "Refresh it with: nf cache occm refresh"
    assert all(r.status is CheckStatus.WARNING for r in rows.values())


def test_newer_schema_is_not_compared(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    path = _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "x")]})])
    conn = sqlite3.connect(path)
    conn.execute("UPDATE _schema_version SET version = ?", (OccmCacheDB.SCHEMA_VERSION + 1,))
    conn.commit()
    conn.close()

    rows = _run(config)

    assert list(rows) == ["console_clusters"]
    assert rows["console_clusters"].status is CheckStatus.WARNING


def test_corrupt_cache_warns(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    path = OccmCacheDB.default_path(config)
    path.parent.mkdir(parents=True)
    path.write_bytes(b"not a database" * 100)

    rows = _run(config)

    assert rows["console_clusters"].status is CheckStatus.WARNING
    assert rows["console_clusters"].hint is not None
    assert "nf cache clear" in rows["console_clusters"].hint


def test_check_never_writes_the_caches(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    occm = _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "x", clusterUuid=U1)]})])
    _make_ontap(config, {"c1": U1})
    ontap = ClusterMetadataDB.default_path(config)
    before = (occm.read_bytes(), ontap.read_bytes())

    _run(config)

    assert (occm.read_bytes(), ontap.read_bytes()) == before


def test_missing_ontap_cache_still_matches_by_ip(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(config, [("a1", None, {ONPREM: [_we("w1", "x", clusterAddress="192.0.2.1")]})])

    assert _run(config)["console_clusters.root.c1"].status is CheckStatus.ERROR


def test_unresolvable_accounts_are_skipped(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    with patch.object(Config, "console_account_scopes", side_effect=ConfigurationError("x")):
        rows = check_console_clusters(config, {}, scope=None, cluster_filter_active=False)

    assert [r.status for r in rows] == [CheckStatus.SKIPPED]


def test_no_console_account_gives_no_rows(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1")})

    assert _run(config) == {}


def test_duplicate_public_id_is_counted_once(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    _make_occm(
        config,
        [("a1", None, {AWS_HA: [_we("w1", "c1")]}), ("a2", None, {AWS_HA: [_we("w1", "c1")]})],
    )

    assert "1 cluster(s)" in _run(config)["console_clusters.root"].label


def test_cluster_from_record_is_defensive() -> None:
    record = {
        "publicId": "w1",
        "name": "fallback",
        "ontapClusterProperties": {"lifs": ["bad", {"ip": "192.0.2.5"}], "nodes": [3, {"lifs": 7}]},
    }

    cluster = cluster_from_record(record, None)

    assert cluster.name is None
    assert cluster.display == "fallback"
    assert cluster.ips == frozenset({"192.0.2.5"})
    assert cluster_from_record({"publicId": "w9"}, None).display == "w9"


def test_run_environment_checks_section_by_api(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": _inv(c1="192.0.2.1"), **CONSOLE})
    clusters = config.get_clusters({})

    def titles(apis: tuple[str, ...]) -> list[str]:
        sections = run_environment_checks(config, scope=None, apis=apis, clusters=clusters)
        return [s.title for s in sections]

    assert "Console clusters" in titles(("ontap",))
    assert "Console clusters" in titles(("console",))
    assert "Console clusters" not in titles(("digitaladvisor",))
