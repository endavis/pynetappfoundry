"""Tests for pynetappfoundry.query.realtime module.

All four public functions route through :class:`DataSource`. These tests
exercise the routing by patching ``pynetappfoundry.query.realtime.DataSource``
at the usage site.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.core.config import Config
from pynetappfoundry.query.realtime import (
    _attr_to_api_path,
    _fetch_realtime_via_data_source,
    _resolve_realtime,
    compare_realtime,
    fetch_realtime,
    fetch_realtime_collection,
    watch_realtime,
)

# ---------------------------------------------------------------------------
# Test model and mapping fixtures
# ---------------------------------------------------------------------------


class FakeVolumeRT(BaseModel):
    """Minimal model for realtime testing."""

    name: str = ""
    uuid: str = ""
    svm_name: str = ""
    iops_read: int = 0
    iops_write: int = 0
    latency_read: int = 0
    status_text: str = ""


def _custom_transform(record: dict[str, Any]) -> int:
    """Test transform that sums two nested values."""
    metric = record.get("metric", {})
    return int(metric.get("iops", {}).get("read", 0)) + int(metric.get("iops", {}).get("write", 0))


FAKE_FIELDS_RT = (
    FieldMapping(cache_attr="name", api_path="name"),
    FieldMapping(cache_attr="uuid", api_path="uuid"),
    FieldMapping(cache_attr="svm_name", api_path="svm.name"),
    FieldMapping(
        cache_attr="iops_read",
        api_path="metric.iops.read",
        default=0,
        cache_strategy="realtime",
    ),
    FieldMapping(
        cache_attr="iops_write",
        api_path="metric.iops.write",
        default=0,
        cache_strategy="realtime",
    ),
    FieldMapping(
        cache_attr="latency_read",
        api_path="statistics.latency_raw.read",
        default=0,
        cache_strategy="realtime",
    ),
    FieldMapping(
        cache_attr="status_text",
        api_path="status.message",
        default="",
        cache_strategy="realtime",
    ),
)

FAKE_MAPPING_RT = TypeMapping(
    name="FakeVolumeRT",
    model_class=FakeVolumeRT,
    api_endpoint="/storage/volumes?fields=*",
    fields=FAKE_FIELDS_RT,
    id_field="name",
)


class FakeNoRealtime(BaseModel):
    """Model with no realtime fields."""

    name: str = ""


FAKE_MAPPING_NO_RT = TypeMapping(
    name="FakeNoRealtime",
    model_class=FakeNoRealtime,
    api_endpoint="/storage/aggregates?fields=*",
    fields=(FieldMapping(cache_attr="name", api_path="name"),),
    id_field="name",
)


class FakeTransformModel(BaseModel):
    """Model with a transform-based realtime field."""

    name: str = ""
    iops_total: int = 0


FAKE_TRANSFORM_FIELDS = (
    FieldMapping(cache_attr="name", api_path="name"),
    FieldMapping(
        cache_attr="iops_total",
        api_path="metric.iops.total",
        default=0,
        cache_strategy="realtime",
        transform=_custom_transform,
    ),
)

FAKE_TRANSFORM_MAPPING = TypeMapping(
    name="FakeTransformModel",
    model_class=FakeTransformModel,
    api_endpoint="/storage/volumes?fields=*",
    fields=FAKE_TRANSFORM_FIELDS,
    id_field="name",
)


CLUSTER = "test-cluster"


@pytest.fixture(autouse=True)
def _register_fake_mappings() -> Any:
    """Register test mappings and clean up after test."""
    model_registry.register_mapping("FakeVolumeRT", FAKE_MAPPING_RT)
    model_registry.register_mapping("FakeNoRealtime", FAKE_MAPPING_NO_RT)
    model_registry.register_mapping("FakeTransformModel", FAKE_TRANSFORM_MAPPING)
    yield
    model_registry._mappings.pop("FakeVolumeRT", None)
    model_registry._mappings.pop("FakeNoRealtime", None)
    model_registry._mappings.pop("FakeTransformModel", None)


@pytest.fixture()
def mock_config() -> MagicMock:
    """Return a mock Config suitable for DataSource construction."""
    return MagicMock(spec=Config)


@pytest.fixture()
def mocked_data_source() -> Any:
    """Patch ``DataSource`` at the realtime module's usage site.

    Yields the patched ``DataSource`` class mock.
    """
    ds_instance = MagicMock()
    builder = MagicMock()
    builder.filter.return_value = builder
    builder.fields.return_value = builder
    builder.__iter__ = lambda self: iter(getattr(self, "_results", []))
    builder._results = []
    ds_instance.query.return_value = builder

    with patch(
        "pynetappfoundry.query.realtime.DataSource",
        return_value=ds_instance,
    ) as ds_cls:
        yield ds_cls


def _set_query_results(mocked_ds_cls: MagicMock, results: list[Any]) -> MagicMock:
    """Attach *results* to the patched DataSource's query builder."""
    ds_instance = mocked_ds_cls.return_value
    builder = ds_instance.query.return_value
    builder._results = results
    return builder


# ---------------------------------------------------------------------------
# _resolve_realtime tests
# ---------------------------------------------------------------------------


class TestResolveRealtime:
    """Tests for _resolve_realtime."""

    def test_resolve_returns_mapping_and_realtime_fields(self) -> None:
        mapping, rt_fields = _resolve_realtime(FakeVolumeRT)
        assert mapping is FAKE_MAPPING_RT
        assert len(rt_fields) == 4
        attrs = {f.cache_attr for f in rt_fields}
        assert attrs == {"iops_read", "iops_write", "latency_read", "status_text"}

    def test_resolve_filters_by_field_names(self) -> None:
        _, rt_fields = _resolve_realtime(FakeVolumeRT, fields=["iops_read"])
        assert len(rt_fields) == 1
        assert rt_fields[0].cache_attr == "iops_read"

    def test_resolve_unknown_model_raises(self) -> None:
        class Unknown(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered for 'Unknown'"):
            _resolve_realtime(Unknown)

    def test_resolve_no_realtime_fields(self) -> None:
        _, rt_fields = _resolve_realtime(FakeNoRealtime)
        assert len(rt_fields) == 0


# ---------------------------------------------------------------------------
# _attr_to_api_path tests
# ---------------------------------------------------------------------------


class TestAttrToApiPath:
    """Tests for _attr_to_api_path."""

    def test_translates_known_attr(self) -> None:
        assert _attr_to_api_path(FAKE_MAPPING_RT, "svm_name") == "svm.name"

    def test_returns_unknown_attr_unchanged(self) -> None:
        assert _attr_to_api_path(FAKE_MAPPING_RT, "unknown_field") == "unknown_field"


# ---------------------------------------------------------------------------
# fetch_realtime tests
# ---------------------------------------------------------------------------


class TestFetchRealtime:
    """Tests for fetch_realtime (returns model instance)."""

    def test_routes_through_datasource_get(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        model_instance = FakeVolumeRT(iops_read=10, iops_write=20, latency_read=5, status_text="ok")
        ds_instance.get.return_value = model_instance
        result = fetch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid")

        mocked_data_source.assert_called_once_with(mock_config)
        ds_instance.get.assert_called_once()
        assert result is model_instance
        assert result.iops_read == 10
        assert result.iops_write == 20

    def test_with_field_filter(self, mock_config: MagicMock, mocked_data_source: MagicMock) -> None:
        ds_instance = mocked_data_source.return_value
        model_instance = FakeVolumeRT(iops_read=42)
        ds_instance.get.return_value = model_instance

        result = fetch_realtime(
            FakeVolumeRT, mock_config, CLUSTER, "test-uuid", fields=["iops_read"]
        )

        assert result is model_instance
        assert result.iops_read == 42
        kwargs = ds_instance.get.call_args.kwargs
        assert kwargs["fields"] == ["iops_read"]

    def test_unknown_model_raises(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        class NotRegistered(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered"):
            fetch_realtime(NotRegistered, mock_config, CLUSTER, "test-uuid")

    def test_no_realtime_fields_returns_none(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        result = fetch_realtime(FakeNoRealtime, mock_config, CLUSTER, "test-uuid")
        assert result is None
        mocked_data_source.assert_not_called()

    def test_no_instance_returned_yields_none(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = None
        result = fetch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid")
        assert result is None

    def test_transform_callback_honored(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        model_instance = FakeTransformModel(iops_total=400)
        ds_instance.get.return_value = model_instance
        result = fetch_realtime(FakeTransformModel, mock_config, CLUSTER, "test-uuid")
        assert result is model_instance
        assert result.iops_total == 400


# ---------------------------------------------------------------------------
# fetch_realtime_collection tests
# ---------------------------------------------------------------------------


class TestFetchRealtimeCollection:
    """Tests for fetch_realtime_collection (returns list of model instances)."""

    def test_routes_through_datasource_query(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        vols = [
            FakeVolumeRT(
                uuid="u1",
                name="vol1",
                iops_read=10,
                iops_write=20,
                latency_read=1,
                status_text="ok",
            ),
            FakeVolumeRT(
                uuid="u2",
                name="vol2",
                iops_read=30,
                iops_write=40,
                latency_read=2,
                status_text="ok",
            ),
        ]
        _set_query_results(mocked_data_source, vols)

        results = fetch_realtime_collection(FakeVolumeRT, mock_config, CLUSTER)

        mocked_data_source.assert_called_once_with(mock_config)
        assert len(results) == 2
        assert results[0].uuid == "u1"
        assert results[0].name == "vol1"
        assert results[0].iops_read == 10
        assert results[1].uuid == "u2"
        assert results[1].iops_read == 30

    def test_with_filters_translates_kwargs_to_api_paths(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        _set_query_results(mocked_data_source, [])
        fetch_realtime_collection(FakeVolumeRT, mock_config, CLUSTER, svm_name="vs1")
        builder = mocked_data_source.return_value.query.return_value
        builder.filter.assert_called_once_with({"svm.name": "vs1"})

    def test_filter_passthrough_for_unknown_attr(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        _set_query_results(mocked_data_source, [])
        fetch_realtime_collection(FakeVolumeRT, mock_config, CLUSTER, unknown_field="xyz")
        builder = mocked_data_source.return_value.query.return_value
        builder.filter.assert_called_once_with({"unknown_field": "xyz"})

    def test_empty_response(self, mock_config: MagicMock, mocked_data_source: MagicMock) -> None:
        _set_query_results(mocked_data_source, [])
        results = fetch_realtime_collection(FakeVolumeRT, mock_config, CLUSTER)
        assert results == []


# ---------------------------------------------------------------------------
# watch_realtime tests
# ---------------------------------------------------------------------------


class TestWatchRealtime:
    """Tests for watch_realtime."""

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_yields_snapshots(
        self,
        mock_sleep: MagicMock,
        mock_config: MagicMock,
        mocked_data_source: MagicMock,
    ) -> None:
        ds_instance = mocked_data_source.return_value
        model_instance = FakeVolumeRT(iops_read=10, iops_write=20)
        ds_instance.get.return_value = model_instance
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=2)
        snapshots = list(gen)
        assert len(snapshots) == 2
        assert snapshots[0]["model"] is model_instance
        assert snapshots[0]["model"].iops_read == 10

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_includes_timestamp(
        self,
        mock_sleep: MagicMock,
        mock_config: MagicMock,
        mocked_data_source: MagicMock,
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=1)
        snapshot = next(gen)
        assert "_timestamp" in snapshot
        assert "T" in snapshot["_timestamp"]

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_respects_count(
        self,
        mock_sleep: MagicMock,
        mock_config: MagicMock,
        mocked_data_source: MagicMock,
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=3)
        snapshots = list(gen)
        assert len(snapshots) == 3
        assert mock_sleep.call_count == 2

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_routes_through_datasource_get(
        self,
        mock_sleep: MagicMock,
        mock_config: MagicMock,
        mocked_data_source: MagicMock,
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=1)
        next(gen)
        ds_instance.get.assert_called_once()
        kwargs = ds_instance.get.call_args.kwargs
        assert kwargs["cluster"] == CLUSTER
        assert kwargs["id"] == "test-uuid"
        assert kwargs["source"] == "live"

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_custom_interval(
        self,
        mock_sleep: MagicMock,
        mock_config: MagicMock,
        mocked_data_source: MagicMock,
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", interval=10, count=2)
        list(gen)
        mock_sleep.assert_called_with(10)

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_builds_one_data_source_for_loop(
        self,
        mock_sleep: MagicMock,
        mock_config: MagicMock,
        mocked_data_source: MagicMock,
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=3)
        list(gen)
        assert mocked_data_source.call_count == 1
        assert ds_instance.get.call_count == 3


# ---------------------------------------------------------------------------
# compare_realtime tests
# ---------------------------------------------------------------------------


class TestCompareRealtime:
    """Tests for compare_realtime."""

    def test_numeric_delta(self, mock_config: MagicMock, mocked_data_source: MagicMock) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(
            iops_read=150, iops_write=250, latency_read=30, status_text="ok"
        )
        baseline = {"iops_read": 100, "iops_write": 200, "latency_read": 20}
        result = compare_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", baseline)
        assert result["iops_read"]["baseline"] == 100
        assert result["iops_read"]["current"] == 150
        assert result["iops_read"]["delta"] == 50
        assert result["iops_write"]["delta"] == 50
        assert result["latency_read"]["delta"] == 10

    def test_non_numeric_no_delta(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(status_text="degraded")
        baseline = {"status_text": "healthy"}
        result = compare_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", baseline)
        assert result["status_text"]["baseline"] == "healthy"
        assert result["status_text"]["current"] == "degraded"
        assert "delta" not in result["status_text"]

    def test_missing_baseline_field(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(
            iops_read=50, iops_write=60, latency_read=10, status_text="ok"
        )
        baseline: dict[str, Any] = {}
        result = compare_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", baseline)
        assert result["iops_read"] == {"current": 50}
        assert "baseline" not in result["iops_read"]

    def test_calls_data_source_get(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        compare_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", {})
        ds_instance.get.assert_called_once()
        kwargs = ds_instance.get.call_args.kwargs
        assert kwargs["cluster"] == CLUSTER
        assert kwargs["id"] == "test-uuid"

    def test_partial_baseline(self, mock_config: MagicMock, mocked_data_source: MagicMock) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(
            iops_read=100, iops_write=200, latency_read=30, status_text="ok"
        )
        baseline = {"iops_read": 50}
        result = compare_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", baseline)
        assert result["iops_read"]["delta"] == 50
        assert result["iops_write"] == {"current": 200}
        assert result["status_text"] == {"current": "ok"}

    def test_returns_empty_when_no_instance(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = None
        result = compare_realtime(
            FakeVolumeRT, mock_config, CLUSTER, "test-uuid", {"iops_read": 50}
        )
        assert result == {}


# ---------------------------------------------------------------------------
# _fetch_realtime_via_data_source tests (internal helper)
# ---------------------------------------------------------------------------


class TestFetchRealtimeViaDataSource:
    """Direct tests for the shared single-resource helper."""

    def test_helper_delegates_to_get(self) -> None:
        ds = MagicMock()
        model_instance = FakeVolumeRT(iops_read=7, iops_write=8)
        ds.get.return_value = model_instance
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _fetch_realtime_via_data_source(ds, FakeVolumeRT, CLUSTER, "uuid-1", rt_fields)
        ds.get.assert_called_once()
        assert result is model_instance
        assert result.iops_read == 7

    def test_helper_returns_none_when_get_returns_none(self) -> None:
        ds = MagicMock()
        ds.get.return_value = None
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _fetch_realtime_via_data_source(ds, FakeVolumeRT, CLUSTER, "uuid-1", rt_fields)
        assert result is None
