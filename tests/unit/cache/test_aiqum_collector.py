"""Tests for AiqumCollector and refresh_aiqum_cache (#1055)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from pynetappfoundry.cache._collector_runner import CollectionError
from pynetappfoundry.cache.aiqum_collector import (
    AIQUM_CACHED_MAPPINGS,
    AiqumCollector,
    _strip_path,
    refresh_aiqum_cache,
)
from pynetappfoundry.cache.aiqum_db import AiqumCacheDB

_ENDPOINTS = {
    "AiqumCluster": "/datacenter/cluster/clusters",
    "AiqumSvm": "/datacenter/svm/svms",
    "AiqumVolume": "/datacenter/storage/volumes",
}


def _client() -> MagicMock:
    client = MagicMock()
    client.get_all_records.side_effect = lambda path, method, **kw: {
        "records": [{"key": f"{path}-1", "name": "n"}]
    }
    return client


def test_cached_mappings() -> None:
    assert AIQUM_CACHED_MAPPINGS == ("AiqumCluster", "AiqumSvm", "AiqumVolume")


def test_collects_three_endpoints() -> None:
    client = _client()
    snapshot = AiqumCollector(client).collect("aiq1")
    assert snapshot.instance == "aiq1"
    assert set(snapshot.records) == set(_ENDPOINTS)
    calls = [(c.args, c.kwargs) for c in client.get_all_records.call_args_list]
    assert calls == [((ep, "GET"), {"query_params": {}}) for ep in _ENDPOINTS.values()]
    assert snapshot.records["AiqumVolume"][0]["key"] == "/datacenter/storage/volumes-1"


def test_unknown_mapping_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Nope"):
        AiqumCollector(_client(), mappings=("Nope",)).collect("aiq1")


@pytest.mark.parametrize(
    "response",
    [{"num_records": 0}, {"records": {"not": "a list"}}],
    ids=["missing-path", "non-list"],
)
def test_bad_response_raises_collection_error(response: dict[str, Any]) -> None:
    client = MagicMock()
    client.get_all_records.return_value = response
    with pytest.raises(CollectionError, match="AiqumCluster"):
        AiqumCollector(client).collect("aiq1")


def test_http_error_raises_collection_error() -> None:
    client = _client()
    client.get_all_records.side_effect = requests.HTTPError("boom")
    with pytest.raises(CollectionError, match="request failed"):
        AiqumCollector(client).collect("aiq1")


def test_realtime_fields_stripped() -> None:
    from pynetappfoundry.cache._registry import model_registry
    from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

    class _Model(MagicMock):
        pass

    mapping = TypeMapping(
        name="FakeAiqumCollect",
        model_class=_Model,
        api_endpoint="/fake",
        api_type="aiqum",
        fields=(
            FieldMapping(cache_attr="name", api_path="name"),
            FieldMapping(cache_attr="load", api_path="perf.load", cache_strategy="realtime"),
        ),
    )
    model_registry.register_mapping("FakeAiqumCollect", mapping)
    try:
        client = MagicMock()
        client.get_all_records.return_value = {
            "records": [{"name": "a", "perf": {"load": 3, "other": 1}}]
        }
        snapshot = AiqumCollector(client, mappings=("FakeAiqumCollect",)).collect("aiq1")
    finally:
        model_registry.unregister_mapping("FakeAiqumCollect")
    assert snapshot.records["FakeAiqumCollect"] == [{"name": "a", "perf": {"other": 1}}]


def test_strip_path_missing_parent_is_noop() -> None:
    record: dict[str, Any] = {"a": 1}
    _strip_path(record, "x.y")
    assert record == {"a": 1}


def test_refresh_writes_to_given_db(tmp_path: Path) -> None:
    with (
        patch("pynetappfoundry.clients.aiqum.api.AIQUMAPIClient", return_value=_client()),
        AiqumCacheDB(db_path=tmp_path / "c.db") as db,
    ):
        snapshot = refresh_aiqum_cache(MagicMock(), "aiq1", db=db)
        assert db.is_collected("aiq1", "AiqumVolume")
        assert len(db.query_records("aiq1", "AiqumVolume", {})) == 1
    assert snapshot.instance == "aiq1"


def test_refresh_default_db_from_config(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    with patch("pynetappfoundry.clients.aiqum.api.AIQUMAPIClient", return_value=_client()):
        refresh_aiqum_cache(config, "aiq1")
    with AiqumCacheDB(config=config) as db:
        assert db.list_instances() == ["aiq1"]


def test_failed_refresh_leaves_db_unchanged(tmp_path: Path) -> None:
    with AiqumCacheDB(db_path=tmp_path / "c.db") as db:
        with patch("pynetappfoundry.clients.aiqum.api.AIQUMAPIClient", return_value=_client()):
            refresh_aiqum_cache(MagicMock(), "aiq1", db=db)
        before = db.query_records("aiq1", "AiqumVolume", {})
        bad = _client()
        bad.get_all_records.side_effect = [
            {"records": [{"key": "new"}]},
            {"records": [{"key": "new"}]},
            requests.HTTPError("boom"),
        ]
        with (
            patch("pynetappfoundry.clients.aiqum.api.AIQUMAPIClient", return_value=bad),
            pytest.raises(CollectionError),
        ):
            refresh_aiqum_cache(MagicMock(), "aiq1", db=db)
        assert db.query_records("aiq1", "AiqumVolume", {}) == before
