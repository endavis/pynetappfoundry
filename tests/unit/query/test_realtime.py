"""Tests for pynetappfoundry.query.realtime module.

Phase 3d of issue #495 (ADR-0012) routes the four public functions
through :class:`DataSource`. These tests exercise the shim by patching
``pynetappfoundry.query.realtime.DataSource`` at the usage site (not
the definition site) — mirroring the 3c ``QuerySet`` shim fixture
pattern.
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
    _model_to_dotted_dict,
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

    Yields the patched ``DataSource`` class mock. Tests can read
    ``.return_value`` to obtain the single mocked ``DataSource`` instance
    that the code under test constructs. The patch also wires
    ``.query(...)`` to a chainable builder mock that supports
    ``.filter()`` / ``.fields()`` and iteration.
    """
    # One shared "instance mock" returned from every DataSource(config) call.
    ds_instance = MagicMock()
    # Chainable QueryBuilder mock: ``.filter`` and ``.fields`` return the
    # same builder so ``.filter(...).fields(...)`` works; iteration yields
    # whatever the test wires up via ``_set_query_results``.
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
# _model_to_dotted_dict tests
# ---------------------------------------------------------------------------


class TestModelToDottedDict:
    """Tests for the model → dotted dict projection helper."""

    def test_dotted_dict_projection_preserves_cache_attr_keys(self) -> None:
        instance = FakeVolumeRT(
            name="v1",
            uuid="u1",
            iops_read=100,
            iops_write=200,
            latency_read=50,
            status_text="ok",
        )
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _model_to_dotted_dict(instance, rt_fields)
        assert set(result.keys()) == {
            "iops_read",
            "iops_write",
            "latency_read",
            "status_text",
        }
        assert result["iops_read"] == 100
        assert result["iops_write"] == 200
        assert result["latency_read"] == 50
        assert result["status_text"] == "ok"

    def test_dotted_dict_returns_empty_for_none_instance(self) -> None:
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        assert _model_to_dotted_dict(None, rt_fields) == {}

    def test_missing_attributes_use_field_defaults(self) -> None:
        """A FieldMapping whose cache_attr does not exist on the model
        falls back to ``field.default``."""
        bogus = FieldMapping(
            cache_attr="not_on_model",
            api_path="x",
            default=-1,
            cache_strategy="realtime",
        )
        instance = FakeVolumeRT(name="v1")
        result = _model_to_dotted_dict(instance, (bogus,))
        assert result == {"not_on_model": -1}


# ---------------------------------------------------------------------------
# fetch_realtime tests
# ---------------------------------------------------------------------------


class TestFetchRealtime:
    """Tests for fetch_realtime (routed through DataSource)."""

    def test_routes_through_datasource_get(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(
            iops_read=10, iops_write=20, latency_read=5, status_text="ok"
        )
        result = fetch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid")

        mocked_data_source.assert_called_once_with(mock_config)
        ds_instance.get.assert_called_once()
        kwargs = ds_instance.get.call_args.kwargs
        assert kwargs["cluster"] == CLUSTER
        assert kwargs["id"] == "test-uuid"
        assert kwargs["source"] == "live"
        # Realtime cache_attrs requested via the fields= kwarg.
        assert set(kwargs["fields"]) == {
            "iops_read",
            "iops_write",
            "latency_read",
            "status_text",
        }
        # Positional arg is the model class.
        assert ds_instance.get.call_args.args[0] is FakeVolumeRT

        assert result["iops_read"] == 10
        assert result["iops_write"] == 20
        assert result["latency_read"] == 5
        assert result["status_text"] == "ok"

    def test_with_field_filter(self, mock_config: MagicMock, mocked_data_source: MagicMock) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(iops_read=42)

        result = fetch_realtime(
            FakeVolumeRT, mock_config, CLUSTER, "test-uuid", fields=["iops_read"]
        )

        assert result == {"iops_read": 42}
        kwargs = ds_instance.get.call_args.kwargs
        assert kwargs["fields"] == ["iops_read"]

    def test_unknown_model_raises(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        class NotRegistered(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered"):
            fetch_realtime(NotRegistered, mock_config, CLUSTER, "test-uuid")

    def test_no_realtime_fields_returns_empty(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        result = fetch_realtime(FakeNoRealtime, mock_config, CLUSTER, "test-uuid")
        assert result == {}
        # DataSource is never constructed when there are no realtime fields.
        mocked_data_source.assert_not_called()

    def test_no_instance_returned_yields_empty_dict(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = None
        result = fetch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid")
        assert result == {}

    def test_missing_values_use_defaults(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        # Instance built with no realtime fields set — all default to 0/"".
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        result = fetch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid")
        assert result["iops_read"] == 0
        assert result["iops_write"] == 0
        assert result["latency_read"] == 0
        assert result["status_text"] == ""

    def test_transform_callback_honored_by_shim(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        """``FieldMapping.transform`` callbacks run inside ``parse_api_response``
        before the model is constructed, so the transformed value is visible
        on the returned instance — the shim's job is just to read it back."""
        ds_instance = mocked_data_source.return_value
        # FakeTransformModel.iops_total is populated by the transform
        # callback; the shim projects whatever attribute is on the model.
        ds_instance.get.return_value = FakeTransformModel(iops_total=400)
        result = fetch_realtime(FakeTransformModel, mock_config, CLUSTER, "test-uuid")
        assert result["iops_total"] == 400


# ---------------------------------------------------------------------------
# fetch_realtime_collection tests
# ---------------------------------------------------------------------------


class TestFetchRealtimeCollection:
    """Tests for fetch_realtime_collection (routed through DataSource.query)."""

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
        ds_instance = mocked_data_source.return_value
        ds_instance.query.assert_called_once()
        kwargs = ds_instance.query.call_args.kwargs
        assert kwargs["cluster"] == CLUSTER
        assert kwargs["source"] == "live"
        assert ds_instance.query.call_args.args[0] is FakeVolumeRT

        builder = ds_instance.query.return_value
        builder.filter.assert_called_once_with({})
        builder.fields.assert_called_once()
        field_args = set(builder.fields.call_args.args)
        # Requested fields include realtime cache_attrs plus uuid/name.
        assert {"iops_read", "iops_write", "latency_read", "status_text"}.issubset(field_args)
        assert "uuid" in field_args
        assert "name" in field_args

        assert len(results) == 2
        assert results[0]["uuid"] == "u1"
        assert results[0]["name"] == "vol1"
        assert results[0]["iops_read"] == 10
        assert results[1]["uuid"] == "u2"
        assert results[1]["iops_read"] == 30

    def test_includes_uuid_and_name(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        _set_query_results(
            mocked_data_source,
            [
                FakeVolumeRT(
                    uuid="abc",
                    name="test_vol",
                    iops_read=1,
                    iops_write=2,
                ),
            ],
        )
        results = fetch_realtime_collection(FakeVolumeRT, mock_config, CLUSTER)
        assert results[0]["uuid"] == "abc"
        assert results[0]["name"] == "test_vol"

    def test_with_filters_translates_kwargs_to_api_paths(
        self, mock_config: MagicMock, mocked_data_source: MagicMock
    ) -> None:
        _set_query_results(mocked_data_source, [])
        fetch_realtime_collection(FakeVolumeRT, mock_config, CLUSTER, svm_name="vs1")
        builder = mocked_data_source.return_value.query.return_value
        # svm_name → svm.name per FAKE_MAPPING_RT.
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
        ds_instance.get.return_value = FakeVolumeRT(iops_read=10, iops_write=20)
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=2)
        snapshots = list(gen)
        assert len(snapshots) == 2
        assert snapshots[0]["iops_read"] == 10

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
        # Sleep is called between iterations (count-1 times).
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
        """Per issue #508 locked decision #2: ``watch_realtime`` must build
        exactly one ``DataSource(config)`` and reuse it across all polls."""
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT()
        gen = watch_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", count=3)
        list(gen)
        # Exactly one DataSource constructed.
        assert mocked_data_source.call_count == 1
        # And three .get() calls against it.
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
        """Baseline has some but not all fields."""
        ds_instance = mocked_data_source.return_value
        ds_instance.get.return_value = FakeVolumeRT(
            iops_read=100, iops_write=200, latency_read=30, status_text="ok"
        )
        baseline = {"iops_read": 50}
        result = compare_realtime(FakeVolumeRT, mock_config, CLUSTER, "test-uuid", baseline)
        assert result["iops_read"]["delta"] == 50
        assert result["iops_write"] == {"current": 200}
        assert result["status_text"] == {"current": "ok"}


# ---------------------------------------------------------------------------
# _fetch_realtime_via_data_source tests (internal helper)
# ---------------------------------------------------------------------------


class TestFetchRealtimeViaDataSource:
    """Direct tests for the shared single-resource helper."""

    def test_helper_delegates_to_get_and_projects(self) -> None:
        ds = MagicMock()
        ds.get.return_value = FakeVolumeRT(iops_read=7, iops_write=8)
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _fetch_realtime_via_data_source(ds, FakeVolumeRT, CLUSTER, "uuid-1", rt_fields)
        ds.get.assert_called_once()
        assert result["iops_read"] == 7
        assert result["iops_write"] == 8

    def test_helper_returns_empty_when_get_returns_none(self) -> None:
        ds = MagicMock()
        ds.get.return_value = None
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _fetch_realtime_via_data_source(ds, FakeVolumeRT, CLUSTER, "uuid-1", rt_fields)
        assert result == {}
