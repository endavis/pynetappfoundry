"""Cache-backed DataSource queries on the AIQUM backend (#1055)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache.aiqum_collector import AiqumSnapshot
from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.aiqum_backend import AiqumBackend
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
    AiqumVolumeMetricsSampleResponse,
)
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.model import AiqumVolume

_CLIENT_PATH = "pynetappfoundry.clients.aiqum.api.AIQUMAPIClient"

_VOLUMES = [
    {"key": "k1", "name": "vol1", "svm": {"name": "vs1"}, "state": "online"},
    {"key": "k2", "name": "vol2", "svm": {"name": "vs2"}, "state": "online"},
]


@pytest.fixture
def cache_db(tmp_path: Path) -> Iterator[AiqumCacheDB]:
    with (
        AiqumCacheDB(db_path=tmp_path / "aiqum_cache.db") as db,
        patch.object(AiqumBackend, "_cache_db", db),
    ):
        yield db


@pytest.fixture
def collected(cache_db: AiqumCacheDB) -> AiqumCacheDB:
    cache_db.set(
        "aiq1",
        AiqumSnapshot(
            instance="aiq1", cached_at=datetime.now(UTC), records={"AiqumVolume": _VOLUMES}
        ),
    )
    return cache_db


@pytest.fixture
def client() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        instance = MagicMock()
        cls.return_value = instance
        instance.cls = cls
        yield instance


def test_cache_source_returns_parsed_records_without_client(
    collected: AiqumCacheDB, client: MagicMock
) -> None:
    results = list(DataSource(MagicMock()).query(AiqumVolume, cluster="aiq1", source="cache"))
    assert [(v.key, v.name) for v in results] == [("k1", "vol1"), ("k2", "vol2")]
    fetched = getattr(results[0], "_fetched_fields", None)
    assert fetched and "name" in fetched
    client.cls.assert_not_called()


def test_cache_filter_uses_json_path(collected: AiqumCacheDB, client: MagicMock) -> None:
    results = list(
        DataSource(MagicMock())
        .query(AiqumVolume, cluster="aiq1", source="cache")
        .filter({"svm.name": "vs2"})
    )
    assert [v.key for v in results] == ["k2"]
    client.cls.assert_not_called()


def test_auto_on_collected_instance_makes_no_live_call(
    collected: AiqumCacheDB, client: MagicMock
) -> None:
    results = list(DataSource(MagicMock()).query(AiqumVolume, cluster="aiq1"))
    assert len(results) == 2
    client.get_all_records.assert_not_called()
    client.cls.assert_not_called()


def test_auto_on_uncollected_instance_falls_back_to_live_once(
    cache_db: AiqumCacheDB, client: MagicMock
) -> None:
    client.get_all_records.return_value = {"records": [_VOLUMES[0]]}
    results = list(DataSource(MagicMock()).query(AiqumVolume, cluster="aiq9"))
    assert [v.key for v in results] == ["k1"]
    client.get_all_records.assert_called_once()


def test_get_cache_hit_makes_no_live_call(collected: AiqumCacheDB, client: MagicMock) -> None:
    vol = DataSource(MagicMock()).get(AiqumVolume, cluster="aiq1", id="k2")
    assert vol is not None
    assert vol.name == "vol2"
    client.call_endpoint.assert_not_called()
    client.get_all_records.assert_not_called()


def test_get_cache_miss_takes_live_item_route(collected: AiqumCacheDB, client: MagicMock) -> None:
    client.api_spec = {"paths": {"/datacenter/storage/volumes/{key}": {"get": {}}}}
    client.call_endpoint.return_value = {"key": "k7", "name": "vol7"}
    vol = DataSource(MagicMock()).get(AiqumVolume, cluster="aiq1", id="k7")
    assert vol is not None
    assert vol.name == "vol7"
    client.call_endpoint.assert_called_once_with(
        "/datacenter/storage/volumes/{key}", path_params={"key": "k7"}
    )
    client.get_all_records.assert_not_called()


def test_metrics_auto_goes_straight_to_live(collected: AiqumCacheDB, client: MagicMock) -> None:
    client.call_endpoint.return_value = {"num_samples": 1}
    list(
        DataSource(MagicMock()).query(
            AiqumVolumeMetricsSampleResponse, cluster="aiq1", path_params={"key": "k1"}
        )
    )
    client.call_endpoint.assert_called_once()


def test_metrics_cache_source_rejected(collected: AiqumCacheDB) -> None:
    with pytest.raises(ValueError, match="live-only"):
        DataSource(MagicMock()).query(
            AiqumVolumeMetricsSampleResponse, cluster="aiq1", source="cache"
        )


def test_per_parent_metrics_still_fetch_parents_live(
    collected: AiqumCacheDB, client: MagicMock
) -> None:
    client.get_all_records.side_effect = [
        {"records": [{"key": "live-parent", "name": "p"}]},
    ]
    client.call_endpoint.return_value = {"num_samples": 1}
    settings = MagicMock(max_parent_requests=0)
    config = MagicMock()
    config.get_aiqum_api_settings.return_value = settings
    list(DataSource(config).query(AiqumVolumeMetricsSampleResponse, cluster="aiq1"))
    client.get_all_records.assert_called_once()
    assert client.get_all_records.call_args.args[0] == "/datacenter/storage/volumes"
    client.call_endpoint.assert_called_once_with(
        "/datacenter/storage/volumes/{key}/metrics",
        query_params={},
        path_params={"key": "live-parent"},
    )


def test_where_still_rejected_at_chain_time(collected: AiqumCacheDB) -> None:
    qb = DataSource(MagicMock()).query(AiqumVolume, cluster="aiq1", source="cache")
    with pytest.raises(ValueError, match="AiqumBackend"):
        qb.where("size > 1")


def test_default_is_live_only_follows_class_flag() -> None:
    from pynetappfoundry.data.backends import OntapBackend
    from pynetappfoundry.data.dii_backend import DiiBackend

    mapping = MagicMock()
    assert OntapBackend.is_live_only(mapping) is False
    assert DiiBackend.is_live_only(mapping) is True


class TestBackendRejections:
    def _decision(self, cache: tuple[str, ...], live: tuple[str, ...]) -> RoutingDecision:
        return RoutingDecision(cache_fields=cache, live_fields=live)

    def _mapping(self, model: type) -> Any:
        from pynetappfoundry.cache._registry import model_registry

        mapping = model_registry.get_mapping_by_model_class(model)
        assert mapping is not None
        return mapping

    def test_cache_with_path_params(self, collected: AiqumCacheDB) -> None:
        backend = AiqumBackend(MagicMock())
        with pytest.raises(ValueError, match="live queries only"):
            backend.query(
                AiqumVolume,
                self._mapping(AiqumVolume),
                self._decision(("name",), ()),
                "aiq1",
                {},
                path_params={"key": "k1"},
            )

    def test_cache_with_parent_filters(self, collected: AiqumCacheDB) -> None:
        backend = AiqumBackend(MagicMock())
        with pytest.raises(ValueError, match="live queries only"):
            backend.query(
                AiqumVolume,
                self._mapping(AiqumVolume),
                self._decision(("name",), ()),
                "aiq1",
                {},
                parent_filters={"x": "y"},
            )

    def test_partial_decision(self, collected: AiqumCacheDB) -> None:
        backend = AiqumBackend(MagicMock())
        with pytest.raises(NotImplementedError, match="partial"):
            backend.query(
                AiqumVolume,
                self._mapping(AiqumVolume),
                self._decision(("name",), ("state",)),
                "aiq1",
                {},
            )

    def test_cache_only_on_uncollected_mapping(self, collected: AiqumCacheDB) -> None:
        backend = AiqumBackend(MagicMock())
        with pytest.raises(NotImplementedError, match="cache-only"):
            backend.query(
                AiqumVolumeMetricsSampleResponse,
                self._mapping(AiqumVolumeMetricsSampleResponse),
                self._decision(("duration",), ()),
                "aiq1",
                {},
            )

    def test_where_expressions(self, collected: AiqumCacheDB) -> None:
        backend = AiqumBackend(MagicMock())
        with pytest.raises(NotImplementedError, match="where_expressions"):
            backend.query(
                AiqumVolume,
                self._mapping(AiqumVolume),
                self._decision(("name",), ()),
                "aiq1",
                {},
                where_expressions=("size > 1",),
            )

    def test_cache_db_built_from_config(self, tmp_path: Path) -> None:
        config = MagicMock()
        config.config_dir = tmp_path
        backend = AiqumBackend(config)
        assert backend._cache_db.db_path == tmp_path / ".cache" / "aiqum_cache.db"
        backend._cache_db.close()
