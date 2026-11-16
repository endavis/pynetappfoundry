"""End-to-end DataSource tests over the generated AIQUM models (mocked client)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.aiqum.admin.datasources.clusters.model import AiqumDatasource
from pynetappfoundry.models.aiqum.datacenter.cluster.clusters.model import AiqumCluster
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.model import AiqumVolume
from pynetappfoundry.models.aiqum.datacenter.svm.svms.model import AiqumSvm

_CLIENT_PATH = "pynetappfoundry.clients.aiqum.api.AIQUMAPIClient"


@pytest.fixture(autouse=True)
def empty_aiqum_cache(tmp_path: Path) -> Iterator[None]:
    """Point the AIQUM cache at an empty file so ``auto`` falls back to live."""
    from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
    from pynetappfoundry.data.aiqum_backend import AiqumBackend

    with (
        AiqumCacheDB(db_path=tmp_path / "aiqum_cache.db") as db,
        patch.object(AiqumBackend, "_cache_db", db),
    ):
        yield


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
    from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
        AiqumVolumeMetricsSampleResponse,
    )

    with pytest.raises(ValueError, match="live-only"):
        DataSource(MagicMock()).query(
            AiqumVolumeMetricsSampleResponse, cluster="aiqum1", source="cache"
        )


def test_where_rejected() -> None:
    qb = DataSource(MagicMock()).query(AiqumVolume, cluster="aiqum1")
    with pytest.raises(ValueError, match="AiqumBackend"):
        qb.where("size > 1")


class TestVolumeMetricsPathParams:
    """The {key}/metrics mapping is queried with path_params (#1054)."""

    def test_metrics_with_path_params(self, client: MagicMock) -> None:
        from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
            AiqumVolumeMetricsSampleResponse,
        )

        client.call_endpoint.return_value = {"num_samples": 2, "duration": "PT1H"}
        ds = DataSource(MagicMock())
        results = list(
            ds.query(
                AiqumVolumeMetricsSampleResponse,
                cluster="aiqum1",
                path_params={"key": "a,b:c=d"},
            ).filter({"interval": "1h"})
        )
        assert [r.num_samples for r in results] == [2]
        client.call_endpoint.assert_called_once_with(
            "/datacenter/storage/volumes/{key}/metrics",
            query_params={"interval": "1h"},
            path_params={"key": "a%2Cb%3Ac%3Dd"},
        )


class TestVolumeMetricsPerParent:
    """The {key}/metrics mapping without path_params fetches per volume (#1057)."""

    def test_metrics_per_volume(self, client: MagicMock) -> None:
        from pynetappfoundry.core.models import AIQUMAPISettings
        from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
            AiqumVolumeMetricsSampleResponse,
        )

        client.get_all_records.return_value = _envelope(
            {"key": "a,b", "name": "v1"}, {"key": "k2", "name": "v2"}
        )
        client.call_endpoint.side_effect = [
            {"num_samples": 1, "duration": "PT1H"},
            {"num_samples": 2, "duration": "PT1H"},
        ]
        config = MagicMock()
        config.get_aiqum_api_settings.return_value = AIQUMAPISettings()
        results = list(
            DataSource(config)
            .query(AiqumVolumeMetricsSampleResponse, cluster="aiqum1")
            .filter({"interval": "1h"})
        )
        assert [r.num_samples for r in results] == [1, 2]
        client.get_all_records.assert_called_once_with(
            "/datacenter/storage/volumes", "GET", query_params={}
        )
        metrics = "/datacenter/storage/volumes/{key}/metrics"
        assert [c.kwargs for c in client.call_endpoint.call_args_list] == [
            {"query_params": {"interval": "1h"}, "path_params": {"key": "a%2Cb"}},
            {"query_params": {"interval": "1h"}, "path_params": {"key": "k2"}},
        ]
        assert all(c.args == (metrics,) for c in client.call_endpoint.call_args_list)

    def test_metrics_with_parent_filters(self, client: MagicMock) -> None:
        from pynetappfoundry.core.models import AIQUMAPISettings
        from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
            AiqumVolumeMetricsSampleResponse,
        )

        client.get_all_records.return_value = _envelope({"key": "k1", "name": "v1"})
        client.call_endpoint.return_value = {"num_samples": 1, "duration": "PT1H"}
        config = MagicMock()
        config.get_aiqum_api_settings.return_value = AIQUMAPISettings()
        results = list(
            DataSource(config)
            .query(
                AiqumVolumeMetricsSampleResponse,
                cluster="aiqum1",
                parent_filters={"svm.name": "vs1"},
            )
            .filter({"interval": "1h"})
        )
        assert [r.num_samples for r in results] == [1]
        client.get_all_records.assert_called_once_with(
            "/datacenter/storage/volumes", "GET", query_params={"svm.name": "vs1"}
        )
        client.call_endpoint.assert_called_once_with(
            "/datacenter/storage/volumes/{key}/metrics",
            query_params={"interval": "1h"},
            path_params={"key": "k1"},
        )


class TestGetByKey:
    """get() and a single key filter use the item endpoint (#1060)."""

    @pytest.fixture
    def item_client(self, client: MagicMock) -> MagicMock:
        client.api_spec = {
            "paths": {
                p: {"get": {}}
                for p in (
                    "/datacenter/storage/volumes/{key}",
                    "/datacenter/svm/svms/{key}",
                    "/datacenter/cluster/clusters/{key}",
                )
            }
        }
        return client

    def test_get_volume(self, item_client: MagicMock) -> None:
        item_client.call_endpoint.return_value = {"key": "a,b:c=d", "name": "vol1", "_links": {}}
        vol = DataSource(MagicMock()).get(AiqumVolume, cluster="aiqum1", id="a,b:c=d")
        assert vol is not None
        assert (vol.key, vol.name) == ("a,b:c=d", "vol1")
        item_client.call_endpoint.assert_called_once_with(
            "/datacenter/storage/volumes/{key}", path_params={"key": "a%2Cb%3Ac%3Dd"}
        )
        item_client.get_all_records.assert_not_called()

    def test_get_svm(self, item_client: MagicMock) -> None:
        item_client.call_endpoint.return_value = {"key": "s1", "name": "vs1"}
        svm = DataSource(MagicMock()).get(AiqumSvm, cluster="aiqum1", id="s1")
        assert svm is not None
        assert svm.name == "vs1"
        item_client.call_endpoint.assert_called_once_with(
            "/datacenter/svm/svms/{key}", path_params={"key": "s1"}
        )

    def test_get_cluster(self, item_client: MagicMock) -> None:
        item_client.call_endpoint.return_value = {"key": "c1", "name": "cl1"}
        cluster = DataSource(MagicMock()).get(AiqumCluster, cluster="aiqum1", id="c1")
        assert cluster is not None
        assert cluster.name == "cl1"
        item_client.call_endpoint.assert_called_once_with(
            "/datacenter/cluster/clusters/{key}", path_params={"key": "c1"}
        )

    def test_get_missing_returns_none(self, item_client: MagicMock) -> None:
        import requests

        resp = MagicMock()
        resp.status_code = 404
        item_client.call_endpoint.side_effect = requests.HTTPError("404", response=resp)
        assert DataSource(MagicMock()).get(AiqumVolume, cluster="aiqum1", id="nope") is None

    def test_filter_key_takes_item_route(self, item_client: MagicMock) -> None:
        item_client.call_endpoint.return_value = {"key": "k1", "name": "vol1"}
        results = list(
            DataSource(MagicMock()).query(AiqumVolume, cluster="aiqum1").filter({"key": "k1"})
        )
        assert [v.key for v in results] == ["k1"]
        item_client.get_all_records.assert_not_called()
