"""Tests for pynetappfoundry.query.realtime module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.query.realtime import (
    _attr_to_api_path,
    _parse_realtime_record,
    _realtime_api_fields,
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
def mock_client() -> MagicMock:
    """Return a mocked API client."""
    return MagicMock(spec=["call_endpoint", "get_all_records"])


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
# _parse_realtime_record tests
# ---------------------------------------------------------------------------


class TestParseRealtimeRecord:
    """Tests for _parse_realtime_record."""

    def test_parses_nested_values(self) -> None:
        record = {
            "metric": {"iops": {"read": 100, "write": 200}},
            "statistics": {"latency_raw": {"read": 50}},
            "status": {"message": "ok"},
        }
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _parse_realtime_record(record, rt_fields)
        assert result["iops_read"] == 100
        assert result["iops_write"] == 200
        assert result["latency_read"] == 50
        assert result["status_text"] == "ok"

    def test_missing_values_use_defaults(self) -> None:
        record: dict[str, Any] = {}
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        result = _parse_realtime_record(record, rt_fields)
        assert result["iops_read"] == 0
        assert result["iops_write"] == 0
        assert result["latency_read"] == 0
        assert result["status_text"] == ""

    def test_transform_is_used(self) -> None:
        record = {"metric": {"iops": {"read": 100, "write": 200}}}
        _, rt_fields = _resolve_realtime(FakeTransformModel)
        result = _parse_realtime_record(record, rt_fields)
        assert result["iops_total"] == 300

    def test_transform_failure_uses_default(self) -> None:
        """When transform raises, fallback to default."""

        def bad_transform(record: dict[str, Any]) -> int:
            msg = "boom"
            raise RuntimeError(msg)

        field = FieldMapping(
            cache_attr="bad",
            api_path="x.y",
            default=-1,
            cache_strategy="realtime",
            transform=bad_transform,
        )
        result = _parse_realtime_record({}, (field,))
        assert result["bad"] == -1


# ---------------------------------------------------------------------------
# _realtime_api_fields tests
# ---------------------------------------------------------------------------


class TestRealtimeApiFields:
    """Tests for _realtime_api_fields."""

    def test_deduplicates_top_level_fields(self) -> None:
        _, rt_fields = _resolve_realtime(FakeVolumeRT)
        api_fields = _realtime_api_fields(rt_fields)
        assert api_fields == ["metric", "statistics", "status"]

    def test_empty_fields(self) -> None:
        assert _realtime_api_fields(()) == []


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
    """Tests for fetch_realtime."""

    def test_calls_api_with_correct_url(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 10, "write": 20}},
            "statistics": {"latency_raw": {"read": 5}},
            "status": {"message": "ok"},
        }
        fetch_realtime(FakeVolumeRT, mock_client, "test-uuid")
        url = mock_client.call_endpoint.call_args[0][0]
        assert "/storage/volumes/test-uuid?" in url
        assert "fields=" in url

    def test_requests_correct_api_fields(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {}
        fetch_realtime(FakeVolumeRT, mock_client, "test-uuid")
        url = mock_client.call_endpoint.call_args[0][0]
        assert "fields=metric,statistics,status" in url

    def test_extracts_values_from_response(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 100, "write": 200}},
            "statistics": {"latency_raw": {"read": 50}},
            "status": {"message": "healthy"},
        }
        result = fetch_realtime(FakeVolumeRT, mock_client, "test-uuid")
        assert result["iops_read"] == 100
        assert result["iops_write"] == 200
        assert result["latency_read"] == 50
        assert result["status_text"] == "healthy"

    def test_with_field_filter(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 42}},
        }
        result = fetch_realtime(FakeVolumeRT, mock_client, "test-uuid", fields=["iops_read"])
        assert result == {"iops_read": 42}
        url = mock_client.call_endpoint.call_args[0][0]
        assert "fields=metric" in url

    def test_unknown_model_raises(self, mock_client: MagicMock) -> None:
        class NotRegistered(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered"):
            fetch_realtime(NotRegistered, mock_client, "test-uuid")

    def test_no_realtime_fields_returns_empty(self, mock_client: MagicMock) -> None:
        result = fetch_realtime(FakeNoRealtime, mock_client, "test-uuid")
        assert result == {}
        mock_client.call_endpoint.assert_not_called()

    def test_with_transform(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 150, "write": 250}},
        }
        result = fetch_realtime(FakeTransformModel, mock_client, "test-uuid")
        assert result["iops_total"] == 400

    def test_missing_values_use_defaults(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {}
        result = fetch_realtime(FakeVolumeRT, mock_client, "test-uuid")
        assert result["iops_read"] == 0
        assert result["iops_write"] == 0
        assert result["latency_read"] == 0
        assert result["status_text"] == ""


# ---------------------------------------------------------------------------
# fetch_realtime_collection tests
# ---------------------------------------------------------------------------


class TestFetchRealtimeCollection:
    """Tests for fetch_realtime_collection."""

    def test_fetches_multiple_records(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = {
            "records": [
                {
                    "uuid": "u1",
                    "name": "vol1",
                    "metric": {"iops": {"read": 10, "write": 20}},
                    "statistics": {"latency_raw": {"read": 1}},
                    "status": {"message": "ok"},
                },
                {
                    "uuid": "u2",
                    "name": "vol2",
                    "metric": {"iops": {"read": 30, "write": 40}},
                    "statistics": {"latency_raw": {"read": 2}},
                    "status": {"message": "ok"},
                },
            ],
        }
        results = fetch_realtime_collection(FakeVolumeRT, mock_client)
        assert len(results) == 2
        assert results[0]["uuid"] == "u1"
        assert results[0]["name"] == "vol1"
        assert results[0]["iops_read"] == 10
        assert results[1]["uuid"] == "u2"

    def test_includes_uuid_and_name(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = {
            "records": [
                {
                    "uuid": "abc",
                    "name": "test_vol",
                    "metric": {"iops": {"read": 1, "write": 2}},
                    "statistics": {"latency_raw": {"read": 0}},
                    "status": {"message": ""},
                },
            ],
        }
        results = fetch_realtime_collection(FakeVolumeRT, mock_client)
        assert results[0]["uuid"] == "abc"
        assert results[0]["name"] == "test_vol"

    def test_with_filters(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = {"records": []}
        fetch_realtime_collection(FakeVolumeRT, mock_client, svm_name="vs1")
        url = mock_client.get_all_records.call_args[0][0]
        assert "svm.name=vs1" in url

    def test_uses_get_all_records(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = {"records": []}
        fetch_realtime_collection(FakeVolumeRT, mock_client)
        mock_client.get_all_records.assert_called_once()

    def test_empty_response(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = {"records": []}
        results = fetch_realtime_collection(FakeVolumeRT, mock_client)
        assert results == []


# ---------------------------------------------------------------------------
# watch_realtime tests
# ---------------------------------------------------------------------------


class TestWatchRealtime:
    """Tests for watch_realtime."""

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_yields_snapshots(self, mock_sleep: MagicMock, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 10, "write": 20}},
            "statistics": {"latency_raw": {"read": 5}},
            "status": {"message": "ok"},
        }
        gen = watch_realtime(FakeVolumeRT, mock_client, "test-uuid", count=2)
        snapshots = list(gen)
        assert len(snapshots) == 2
        assert snapshots[0]["iops_read"] == 10

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_includes_timestamp(self, mock_sleep: MagicMock, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 1, "write": 2}},
            "statistics": {"latency_raw": {"read": 0}},
            "status": {"message": ""},
        }
        gen = watch_realtime(FakeVolumeRT, mock_client, "test-uuid", count=1)
        snapshot = next(gen)
        assert "_timestamp" in snapshot
        # Should be ISO format string
        assert "T" in snapshot["_timestamp"]

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_respects_count(self, mock_sleep: MagicMock, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 1, "write": 2}},
            "statistics": {"latency_raw": {"read": 0}},
            "status": {"message": ""},
        }
        gen = watch_realtime(FakeVolumeRT, mock_client, "test-uuid", count=3)
        snapshots = list(gen)
        assert len(snapshots) == 3
        # Sleep called between iterations (count-1 times)
        assert mock_sleep.call_count == 2

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_calls_fetch_realtime(self, mock_sleep: MagicMock, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 1, "write": 2}},
            "statistics": {"latency_raw": {"read": 0}},
            "status": {"message": ""},
        }
        gen = watch_realtime(FakeVolumeRT, mock_client, "test-uuid", count=1)
        next(gen)
        mock_client.call_endpoint.assert_called_once()
        url = mock_client.call_endpoint.call_args[0][0]
        assert "/storage/volumes/test-uuid?" in url

    @patch("pynetappfoundry.query.realtime.time.sleep")
    def test_custom_interval(self, mock_sleep: MagicMock, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 1, "write": 2}},
            "statistics": {"latency_raw": {"read": 0}},
            "status": {"message": ""},
        }
        gen = watch_realtime(FakeVolumeRT, mock_client, "test-uuid", interval=10, count=2)
        list(gen)
        mock_sleep.assert_called_with(10)


# ---------------------------------------------------------------------------
# compare_realtime tests
# ---------------------------------------------------------------------------


class TestCompareRealtime:
    """Tests for compare_realtime."""

    def test_numeric_delta(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 150, "write": 250}},
            "statistics": {"latency_raw": {"read": 30}},
            "status": {"message": "ok"},
        }
        baseline = {"iops_read": 100, "iops_write": 200, "latency_read": 20}
        result = compare_realtime(FakeVolumeRT, mock_client, "test-uuid", baseline)
        assert result["iops_read"]["baseline"] == 100
        assert result["iops_read"]["current"] == 150
        assert result["iops_read"]["delta"] == 50
        assert result["iops_write"]["delta"] == 50
        assert result["latency_read"]["delta"] == 10

    def test_non_numeric_no_delta(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 0, "write": 0}},
            "statistics": {"latency_raw": {"read": 0}},
            "status": {"message": "degraded"},
        }
        baseline = {"status_text": "healthy"}
        result = compare_realtime(FakeVolumeRT, mock_client, "test-uuid", baseline)
        assert result["status_text"]["baseline"] == "healthy"
        assert result["status_text"]["current"] == "degraded"
        assert "delta" not in result["status_text"]

    def test_missing_baseline_field(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 50, "write": 60}},
            "statistics": {"latency_raw": {"read": 10}},
            "status": {"message": "ok"},
        }
        baseline: dict[str, Any] = {}  # No baseline values
        result = compare_realtime(FakeVolumeRT, mock_client, "test-uuid", baseline)
        assert result["iops_read"] == {"current": 50}
        assert "baseline" not in result["iops_read"]

    def test_calls_fetch_realtime(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 1, "write": 2}},
            "statistics": {"latency_raw": {"read": 0}},
            "status": {"message": ""},
        }
        compare_realtime(FakeVolumeRT, mock_client, "test-uuid", {})
        mock_client.call_endpoint.assert_called_once()
        url = mock_client.call_endpoint.call_args[0][0]
        assert "/storage/volumes/test-uuid?" in url

    def test_partial_baseline(self, mock_client: MagicMock) -> None:
        """Baseline has some but not all fields."""
        mock_client.call_endpoint.return_value = {
            "metric": {"iops": {"read": 100, "write": 200}},
            "statistics": {"latency_raw": {"read": 30}},
            "status": {"message": "ok"},
        }
        baseline = {"iops_read": 50}
        result = compare_realtime(FakeVolumeRT, mock_client, "test-uuid", baseline)
        # Field in baseline: has baseline, current, delta
        assert result["iops_read"]["delta"] == 50
        # Field not in baseline: current only
        assert result["iops_write"] == {"current": 200}
        assert result["status_text"] == {"current": "ok"}
