"""End-to-end DataSource tests over the generated AIQUM models (mocked client)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.aiqum.admin.datasources.clusters.model import AiqumDatasource
from pynetappfoundry.models.aiqum.datacenter.cluster.clusters.model import AiqumCluster
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.model import AiqumVolume
from pynetappfoundry.models.aiqum.datacenter.svm.svms.model import AiqumSvm

_CLIENT_PATH = "pynetappfoundry.clients.aiqum.api.AIQUMAPIClient"


@pytest.fixture
def client() -> Iterator[MagicMock]:
    """Patch AIQUMAPIClient so no HTTP or config is needed."""
    with patch(_CLIENT_PATH) as cls:
        instance = MagicMock()
        cls.return_value = instance
        instance.cls = cls
        yield instance


def _envelope(*records: dict[str, Any]) -> dict[str, Any]:
    return {"num_records": len(records), "records": list(records)}


def test_mappings_are_aiqum() -> None:
    ds = DataSource(MagicMock())
    for model in (AiqumCluster, AiqumSvm, AiqumVolume, AiqumDatasource):
        assert ds._resolve_mapping(model).api_type == "aiqum"


def test_volumes_with_filter(client: MagicMock) -> None:
    client.get_all_records.return_value = _envelope(
        {"key": "k1", "name": "vol1", "svm": {"name": "vs1"}, "state": "online"}
    )
    ds = DataSource(MagicMock())
    results = list(ds.query(AiqumVolume, cluster="aiqum1").filter({"svm.name": "vs1"}))
    assert [(v.key, v.name, v.svm.name) for v in results] == [("k1", "vol1", "vs1")]
    client.get_all_records.assert_called_once_with(
        "/datacenter/storage/volumes", "GET", query_params={"svm.name": "vs1"}
    )
    client.cls.assert_called_once()
    assert client.cls.call_args.args[0] == "aiqum1"


def test_svms(client: MagicMock) -> None:
    client.get_all_records.return_value = _envelope(
        {"key": "s1", "name": "vs1", "state": "running", "cluster": {"name": "c1"}}
    )
    results = list(DataSource(MagicMock()).query(AiqumSvm, cluster="aiqum1"))
    assert results[0].name == "vs1"
    assert results[0].cluster.name == "c1"


def test_clusters(client: MagicMock) -> None:
    client.get_all_records.return_value = _envelope({"key": "c1", "name": "cl1"})
    results = list(DataSource(MagicMock()).query(AiqumCluster, cluster="aiqum1"))
    assert [c.name for c in results] == ["cl1"]


def test_datasources_smoke(client: MagicMock) -> None:
    client.get_all_records.return_value = _envelope({"key": "d1", "address": "10.0.0.9"})
    results = list(DataSource(MagicMock()).query(AiqumDatasource, cluster="aiqum1"))
    assert results[0].address == "10.0.0.9"


def test_cache_source_rejected() -> None:
    with pytest.raises(ValueError, match="live-only"):
        DataSource(MagicMock()).query(AiqumVolume, cluster="aiqum1", source="cache")


def test_where_rejected() -> None:
    qb = DataSource(MagicMock()).query(AiqumVolume, cluster="aiqum1")
    with pytest.raises(ValueError, match="AiqumBackend"):
        qb.where("size > 1")
