"""Tests for the cross-cache cluster resolver (#1097, ADR-0031)."""

from __future__ import annotations

import ast
import types
import typing
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

import pynetappfoundry.cache.cluster_resolver as resolver_module
from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.aiqum_collector import AIQUM_CACHED_MAPPINGS, AiqumSnapshot
from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
from pynetappfoundry.cache.cluster_resolver import (
    LINK_RULES,
    ClusterResolver,
)
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.occm_collector import (
    OCCM_WORKING_ENVIRONMENT_MAPPINGS,
    OccmAgentSnapshot,
    OccmSnapshot,
)
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.console.discovery import AccountInventory, ConsoleInventory
from pynetappfoundry.models.console_types import ConsoleAgentInfo
from pynetappfoundry.models.ontap.cluster.model import OntapCluster

UUID = "11111111-1111-1111-1111-111111111111"
OTHER_UUID = "22222222-2222-2222-2222-222222222222"
ON_PREM = "OccmOnpremWorkingEnvironment"
CLOUD = tuple(m for m in OCCM_WORKING_ENVIRONMENT_MAPPINGS if m != ON_PREM)


def _we(
    public_id: str, uuid: str | None = UUID, name: str = "lab1", path: str = "ontap"
) -> dict[str, Any]:
    props: dict[str, Any] = {"clusterName": name}
    if uuid is not None:
        props["clusterUuid"] = uuid
    key = "ontapClusterProperties" if path == "ontap" else "clusterProperties"
    return {"publicId": public_id, "name": f"n-{public_id}", key: props}


def _aiq_cluster(key: str, uuid: str | None = UUID, name: str = "lab1") -> dict[str, Any]:
    rec: dict[str, Any] = {"key": key, "name": name}
    if uuid is not None:
        rec["uuid"] = uuid
    return rec


def _aiq_child(key: str, cluster_key: str) -> dict[str, Any]:
    return {"key": key, "name": f"n-{key}", "cluster": {"key": cluster_key}}


def _aiq_snapshot(
    instance: str, records: dict[str, list[dict[str, Any]]], at: datetime | None = None
) -> AiqumSnapshot:
    return AiqumSnapshot(instance=instance, cached_at=at or datetime.now(UTC), records=records)


def _occm_snapshot(
    agents: dict[str, dict[str, list[dict[str, Any]]]],
    inventory: ConsoleInventory | None = None,
    at: datetime | None = None,
) -> OccmSnapshot:
    when = at or datetime.now(UTC)
    return OccmSnapshot(
        cached_at=when,
        inventory=inventory or ConsoleInventory(),
        agents=tuple(
            OccmAgentSnapshot(
                agent_id=a, scope=None, organization_id="org", cached_at=when, records=r
            )
            for a, r in agents.items()
        ),
        failed_agents=(),
        skipped_agents=(),
    )


def _ontap_metadata(
    name: str = "lab1", uuid: str = UUID, real_name: str | None = None
) -> CachedClusterMetadata:
    return CachedClusterMetadata(
        cluster_name=name, cluster=OntapCluster(name=real_name or name, uuid=uuid)
    )


@pytest.fixture
def ontap_db() -> Iterator[ClusterMetadataDB]:
    with ClusterMetadataDB(db_path=":memory:") as db:
        yield db


@pytest.fixture
def aiqum_db(tmp_path: Path) -> Iterator[AiqumCacheDB]:
    with AiqumCacheDB(db_path=tmp_path / "aiqum_cache.db") as db:
        yield db


@pytest.fixture
def occm_db(tmp_path: Path) -> Iterator[OccmCacheDB]:
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db:
        yield db


@pytest.fixture
def full(
    ontap_db: ClusterMetadataDB, aiqum_db: AiqumCacheDB, occm_db: OccmCacheDB
) -> ClusterResolver:
    ontap_db.set("lab1", _ontap_metadata())
    aiqum_db.set(
        "aiq1",
        _aiq_snapshot(
            "aiq1",
            {
                "AiqumCluster": [_aiq_cluster("ck1"), _aiq_cluster("ck2", OTHER_UUID, "other")],
                "AiqumSvm": [_aiq_child("s1", "ck1"), _aiq_child("s2", "ck2")],
                "AiqumVolume": [_aiq_child("v1", "ck1"), _aiq_child("v2", "ck2")],
            },
        ),
    )
    occm_db.set(
        _occm_snapshot({"agent-1": {ON_PREM: [_we("we1"), _we("we2", OTHER_UUID, "other")]}})
    )
    return ClusterResolver(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db)


def test_found_in_every_source_by_uuid(full: ClusterResolver) -> None:
    loc = full.resolve("lab1")
    assert loc.found
    assert loc.cluster_uuid == UUID
    assert loc.ontap is not None
    assert loc.ontap.cluster_name == "lab1"
    assert [(a.instance, a.cluster_key, a.matched_by) for a in loc.aiqum] == [
        ("aiq1", "ck1", "uuid")
    ]
    assert [(o.agent_id, o.mapping, o.public_id, o.matched_by) for o in loc.occm] == [
        ("agent-1", ON_PREM, "we1", "uuid")
    ]


def test_on_prem_uuid_only_under_cluster_properties(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("lab1", _ontap_metadata())
    occm_db.set(_occm_snapshot({"a": {ON_PREM: [_we("we1", path="plain", name="zzz")]}}))
    loc = ClusterResolver(ontap_db=ontap_db, occm_db=occm_db).resolve("lab1")
    assert [o.public_id for o in loc.occm] == ["we1"]
    assert loc.occm[0].matched_by == "uuid"


@pytest.mark.parametrize("mapping", CLOUD)
def test_each_cloud_mapping_matches_on_uuid(
    mapping: str, ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("lab1", _ontap_metadata())
    occm_db.set(_occm_snapshot({"a": {mapping: [_we("we1", name="zzz")]}}))
    loc = ClusterResolver(ontap_db=ontap_db, occm_db=occm_db).resolve("lab1")
    assert [(o.mapping, o.matched_by) for o in loc.occm] == [(mapping, "uuid")]


@pytest.mark.parametrize("mapping", CLOUD)
def test_cloud_record_without_cluster_properties_matches_by_its_own_name(
    mapping: str, ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("lab1", _ontap_metadata())
    record = {"publicId": "we1", "name": "lab1", "ontapClusterProperties": {}}
    other = {"publicId": "we2", "name": "other", "ontapClusterProperties": {}}
    occm_db.set(_occm_snapshot({"a": {mapping: [record, other]}}))
    loc = ClusterResolver(ontap_db=ontap_db, occm_db=occm_db).resolve("lab1")
    assert [(o.public_id, o.matched_by) for o in loc.occm] == [("we1", "name")]


def test_on_prem_record_is_not_matched_by_its_display_name(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("lab1", _ontap_metadata())
    occm_db.set(_occm_snapshot({"a": {ON_PREM: [{"publicId": "we1", "name": "lab1"}]}}))
    loc = ClusterResolver(ontap_db=ontap_db, occm_db=occm_db).resolve("lab1")
    assert loc.occm == ()


def test_name_fallback_for_record_without_uuid_uses_ontap_cluster_name(
    ontap_db: ClusterMetadataDB, aiqum_db: AiqumCacheDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("inv-key", _ontap_metadata("inv-key", real_name="real"))
    aiqum_db.set(
        "aiq1", _aiq_snapshot("aiq1", {"AiqumCluster": [_aiq_cluster("ck1", None, "real")]})
    )
    occm_db.set(_occm_snapshot({"a": {ON_PREM: [_we("we1", None, "real")]}}))
    loc = ClusterResolver(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db).resolve("inv-key")
    assert loc.ontap is not None
    assert loc.ontap.ontap_cluster_name == "real"
    assert [a.matched_by for a in loc.aiqum] == ["name"]
    assert [o.matched_by for o in loc.occm] == ["name"]


def test_same_name_different_uuid_does_not_match(
    ontap_db: ClusterMetadataDB, aiqum_db: AiqumCacheDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("lab1", _ontap_metadata())
    aiqum_db.set(
        "aiq1", _aiq_snapshot("aiq1", {"AiqumCluster": [_aiq_cluster("ck1", OTHER_UUID, "lab1")]})
    )
    occm_db.set(_occm_snapshot({"a": {ON_PREM: [_we("we1", OTHER_UUID, "lab1")]}}))
    loc = ClusterResolver(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db).resolve("lab1")
    assert loc.aiqum == ()
    assert loc.occm == ()
    assert loc.ontap is not None


def test_ontap_cache_absent_matches_by_name(aiqum_db: AiqumCacheDB, occm_db: OccmCacheDB) -> None:
    aiqum_db.set(
        "aiq1", _aiq_snapshot("aiq1", {"AiqumCluster": [_aiq_cluster("ck1", OTHER_UUID, "lab1")]})
    )
    occm_db.set(_occm_snapshot({"a": {ON_PREM: [_we("we1", UUID, "lab1")]}}))
    loc = ClusterResolver(aiqum_db=aiqum_db, occm_db=occm_db).resolve("lab1")
    assert loc.ontap is None
    assert loc.cluster_uuid is None
    assert [a.matched_by for a in loc.aiqum] == ["name"]
    assert [o.matched_by for o in loc.occm] == ["name"]


def test_missing_from_one_source(full: ClusterResolver, aiqum_db: AiqumCacheDB) -> None:
    aiqum_db.clear()
    loc = full.resolve("lab1")
    assert loc.aiqum == ()
    assert loc.ontap is not None
    assert loc.occm


def test_several_instances_and_agents(
    ontap_db: ClusterMetadataDB, aiqum_db: AiqumCacheDB, occm_db: OccmCacheDB
) -> None:
    ontap_db.set("lab1", _ontap_metadata())
    for inst in ("aiq2", "aiq1"):
        aiqum_db.set(inst, _aiq_snapshot(inst, {"AiqumCluster": [_aiq_cluster(f"k-{inst}")]}))
    inventory = ConsoleInventory(
        accounts=[
            AccountInventory(
                scope=scope,
                agents=[ConsoleAgentInfo(agentId="agent-a", name="alpha", scope=scope)],
            )
            for scope in (None, "Acct")
        ]
    )
    occm_db.set(
        _occm_snapshot(
            {"agent-b": {ON_PREM: [_we("we1")]}, "agent-a": {ON_PREM: [_we("we1")]}},
            inventory=inventory,
        )
    )
    loc = ClusterResolver(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db).resolve("lab1")
    assert [a.instance for a in loc.aiqum] == ["aiq1", "aiq2"]
    assert [(o.agent_id, o.public_id) for o in loc.occm] == [("agent-a", "we1"), ("agent-b", "we1")]
    assert loc.occm[0].agent_name == "alpha"
    assert loc.occm[0].scopes == (None, "Acct")
    assert loc.occm[1].agent_name is None


def test_unknown_cluster_is_all_absent(full: ClusterResolver) -> None:
    loc = full.resolve("nope")
    assert not loc.found
    assert loc.ontap is None
    assert loc.aiqum == ()
    assert loc.occm == ()
    data = full.read("nope")
    assert data.ontap is None
    assert data.aiqum == ()
    assert data.occm == ()


@pytest.mark.parametrize("name", ["", "1bad", "a b", "x;drop"])
def test_invalid_name_raises_with_every_db_none(name: str) -> None:
    with pytest.raises(ValueError, match="Invalid cluster name"):
        ClusterResolver().resolve(name)
    with pytest.raises(ValueError, match="Invalid cluster name"):
        ClusterResolver().read(name)


def test_from_config_with_no_cache_files_creates_nothing(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    with ClusterResolver.from_config(config) as resolver:
        assert not resolver.resolve("lab1").found
    assert list(tmp_path.iterdir()) == []


def test_from_config_opens_existing_files_and_closes_them(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    cache = tmp_path / ".cache"
    cache.mkdir()
    with ClusterMetadataDB(db_path=cache / "cluster_metadata.db") as db:
        db.set("lab1", _ontap_metadata())
    with ClusterResolver.from_config(config) as resolver:
        assert resolver.resolve("lab1").ontap is not None
        opened = list(resolver._owned)
    assert len(opened) == 1
    with pytest.raises(Exception, match="closed"):
        opened[0].conn.execute("SELECT 1")


def _field_models(annotation: Any) -> list[type[BaseModel]]:
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return [annotation]
    if typing.get_origin(annotation) in (typing.Union, types.UnionType):
        return [m for arg in typing.get_args(annotation) for m in _field_models(arg)]
    return []


def _path_resolves(model: type[BaseModel], path: str) -> bool:
    head, _, rest = path.partition(".")
    field = model.model_fields.get(head)
    if field is None:
        return False
    if not rest:
        return True
    return any(_path_resolves(m, rest) for m in _field_models(field.annotation))


def test_link_rules_cover_exactly_the_known_mappings() -> None:
    assert set(LINK_RULES) == {"AiqumCluster", *OCCM_WORKING_ENVIRONMENT_MAPPINGS}


@pytest.mark.parametrize("mapping", sorted(LINK_RULES))
def test_link_rule_paths_resolve_against_the_model(mapping: str) -> None:
    mp = model_registry.get_mapping(mapping)
    assert mp is not None
    rule = LINK_RULES[mapping]
    for path in (*rule.uuid_paths, *rule.name_paths):
        assert _path_resolves(mp.model_class, path), path


def test_reader_returns_each_source_with_age(full: ClusterResolver) -> None:
    data = full.read("lab1")
    assert data.ontap is not None
    assert data.ontap.metadata.cluster_name == "lab1"
    assert data.ontap.is_stale is False
    assert len(data.aiqum) == 1
    part = data.aiqum[0]
    assert [getattr(s, "key") for s in part.svms] == ["s1"]  # noqa: B009  # BaseModel has no key attr
    assert [getattr(v, "key") for v in part.volumes] == ["v1"]  # noqa: B009  # BaseModel has no key attr
    assert getattr(part.cluster, "uuid") == UUID  # noqa: B009  # BaseModel has no uuid attr
    assert part.is_stale is False
    assert len(data.occm) == 1
    cls = model_registry.get_mapping(ON_PREM)
    assert cls is not None
    assert isinstance(data.occm[0].record, cls.model_class)
    assert data.occm[0].is_stale is False
    assert data.occm[0].cached_at.tzinfo is not None


def test_reader_returns_stale_data(
    ontap_db: ClusterMetadataDB, aiqum_db: AiqumCacheDB, occm_db: OccmCacheDB
) -> None:
    old = datetime.now(UTC) - timedelta(days=90)
    meta = _ontap_metadata()
    meta.cached_at = old
    ontap_db.set("lab1", meta)
    aiqum_db.set("aiq1", _aiq_snapshot("aiq1", {"AiqumCluster": [_aiq_cluster("ck1")]}, old))
    occm_db.set(_occm_snapshot({"a": {ON_PREM: [_we("we1")]}}, at=old))
    data = ClusterResolver(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db).read("lab1")
    assert data.ontap is not None
    assert data.ontap.is_stale
    assert data.aiqum[0].is_stale
    assert data.occm[0].is_stale
    assert (
        not ClusterResolver(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db)
        .read("lab1", ttl_days=365)
        .aiqum[0]
        .is_stale
    )


def test_reader_keeps_ontap_cloud_metadata_and_occm_cloud_record(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    from pynetappfoundry.cache._metadata import CloudMetadata

    meta = _ontap_metadata()
    meta.cloud = [CloudMetadata(provider="AWS", region="us-east-1")]
    ontap_db.set("lab1", meta)
    occm_db.set(_occm_snapshot({"a": {CLOUD[0]: [_we("we1")]}}))
    data = ClusterResolver(ontap_db=ontap_db, occm_db=occm_db).read("lab1")
    assert data.ontap is not None
    assert data.ontap.metadata.cloud
    assert [o.location.mapping for o in data.occm] == [CLOUD[0]]


def test_module_imports_no_data_or_client_layer() -> None:
    tree = ast.parse(Path(resolver_module.__file__ or "").read_text(encoding="utf-8"))
    imported = [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)] + [
        a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names
    ]
    assert not [
        m for m in imported if m.startswith(("pynetappfoundry.data", "pynetappfoundry.clients"))
    ]
    assert AIQUM_CACHED_MAPPINGS  # the module's AIQUM mappings come from the collector constant


def test_resolve_and_read_make_no_live_call(full: ClusterResolver) -> None:
    boom = RuntimeError("live call")
    with (
        patch(
            "pynetappfoundry.clients.console.agent.ConsoleAgentClient", side_effect=boom
        ) as console,
        patch("pynetappfoundry.clients.aiqum.api.AIQUMAPIClient", side_effect=boom) as aiqum,
        patch(
            "pynetappfoundry.clients.ontap.api.OntapAPIClient", side_effect=boom, create=True
        ) as ontap,
        patch("socket.socket.connect", side_effect=boom) as connect,
    ):
        full.resolve("lab1")
        full.read("lab1")
    for mock in (console, aiqum, ontap, connect):
        mock.assert_not_called()
