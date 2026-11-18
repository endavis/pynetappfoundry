"""AIQUM models accept null for declared fields (#1102).

Records are synthetic: placeholder keys and names only.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.aiqum_collector import AiqumSnapshot
from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
from pynetappfoundry.data.aiqum_backend import AiqumBackend
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models._base import AiqumModel
from pynetappfoundry.models.aiqum.datacenter.cluster.clusters.model import AiqumCluster
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.model import AiqumVolume
from pynetappfoundry.models.aiqum.datacenter.svm.svms.model import AiqumSvm

_CLIENT_PATH = "pynetappfoundry.clients.aiqum.api.AIQUMAPIClient"

_CLUSTER: dict[str, Any] = {
    "key": "ck1",
    "name": "c1",
    "contact": None,
    "location": None,
    "nodes": [{"key": "n1", "name": "node1", "location": None}],
}
_SVM: dict[str, Any] = {
    "key": "s1",
    "name": "vs1",
    "language": None,
    "cifs": {"ad_domain": {"fqdn": None}},
    "fcp": {"enabled": None},
    "iscsi": {"enabled": None},
    "ldap": {"enabled": None},
    "nfs": {"enabled": None},
    "nis": {"domain": None, "enabled": None, "servers": None},
    "nvme": {"enabled": None},
    "snapshot_policy": {"uuid": None, "name": "pol"},
}
_VOLUME: dict[str, Any] = {
    "key": "v1",
    "name": "vol1",
    "snapshot_policy": {"uuid": None, "name": "pol"},
    "qos": None,
}


@pytest.fixture
def cache_db(tmp_path: Path) -> Iterator[AiqumCacheDB]:
    with (
        AiqumCacheDB(db_path=tmp_path / "aiqum_cache.db") as db,
        patch.object(AiqumBackend, "_cache_db", db),
    ):
        yield db


@pytest.fixture
def client() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        instance = MagicMock()
        cls.return_value = instance
        yield instance


def _query(
    model: type[BaseModel],
    record: dict[str, Any],
    source: Literal["cache", "live"],
    cache_db: AiqumCacheDB,
    client: MagicMock,
) -> Any:
    if source == "cache":
        cache_db.set(
            "aiq1",
            AiqumSnapshot(
                instance="aiq1",
                cached_at=datetime.now(UTC),
                records={model.__name__: [record]},
            ),
        )
    else:
        client.get_all_records.return_value = {"num_records": 1, "records": [record]}
    results = list(DataSource(MagicMock()).query(model, cluster="aiq1", source=source))
    assert len(results) == 1
    return results[0]


@pytest.mark.parametrize("source", ["cache", "live"])
def test_cluster_null_contact_and_location(
    source: Literal["cache", "live"], cache_db: AiqumCacheDB, client: MagicMock
) -> None:
    cluster = _query(AiqumCluster, _CLUSTER, source, cache_db, client)
    assert (cluster.contact, cluster.location) == ("", "")
    assert cluster.key == "ck1"
    assert [(n.name, n.location) for n in cluster.nodes] == [("node1", "")]


@pytest.mark.parametrize("source", ["cache", "live"])
def test_svm_null_fields(
    source: Literal["cache", "live"], cache_db: AiqumCacheDB, client: MagicMock
) -> None:
    svm = _query(AiqumSvm, _SVM, source, cache_db, client)
    assert svm.language == ""
    assert svm.cifs.ad_domain.fqdn == ""
    assert (svm.fcp.enabled, svm.iscsi.enabled, svm.ldap.enabled) == (False, False, False)
    assert (svm.nfs.enabled, svm.nvme.enabled) == (False, False)
    assert (svm.nis.domain, svm.nis.enabled, svm.nis.servers) == ("", False, [])
    assert svm.snapshot_policy.uuid == ""
    assert svm.snapshot_policy.name == "pol"
    assert svm.name == "vs1"


@pytest.mark.parametrize("source", ["cache", "live"])
def test_volume_null_fields(
    source: Literal["cache", "live"], cache_db: AiqumCacheDB, client: MagicMock
) -> None:
    volume = _query(AiqumVolume, _VOLUME, source, cache_db, client)
    assert volume.snapshot_policy.uuid == ""
    assert volume.snapshot_policy.name == "pol"
    assert volume.qos == AiqumVolume.model_fields["qos"].annotation()  # type: ignore[misc]  # default sub-model
    assert volume.name == "vol1"


def _aiqum_models() -> list[type[BaseModel]]:
    return sorted(
        (m.model_class for m in model_registry.mappings.values() if m.api_type == "aiqum"),
        key=lambda c: c.__name__,
    )


def _reachable(model: type[BaseModel], seen: set[type[BaseModel]]) -> None:
    if model in seen:
        return
    seen.add(model)
    for field in model.model_fields.values():
        for arg in (field.annotation, *getattr(field.annotation, "__args__", ())):
            if isinstance(arg, type) and issubclass(arg, BaseModel):
                _reachable(arg, seen)


def test_sweep_finds_aiqum_models() -> None:
    assert len(_aiqum_models()) > 3


@pytest.mark.parametrize("model", _aiqum_models(), ids=lambda c: c.__name__)
def test_every_aiqum_model_accepts_all_null_fields(model: type[BaseModel]) -> None:
    assert issubclass(model, AiqumModel)
    model.model_validate(dict.fromkeys(model.model_fields))
    seen: set[type[BaseModel]] = set()
    _reachable(model, seen)
    for sub in seen:
        assert issubclass(sub, AiqumModel), sub
        sub.model_validate(dict.fromkeys(sub.model_fields))
