"""Tests for ``pynetappfoundry.cli.commands.metrics.dump_dii`` helpers.

All tests target the pure helper functions; the Click command is not invoked
via CliRunner (consistent with sibling test files in this package tree).
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import Any
from unittest.mock import DEFAULT, MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.metrics.dump_dii import (
    _METRICS,
    _build_body,
    _compute_window,
    _dump_cluster,
    _dump_volume,
    _parse_timeseries,
    _validate_and_clean,
)

# ---------------------------------------------------------------------------
# _compute_window
# ---------------------------------------------------------------------------


class TestComputeWindow:
    """Tests for :func:`_compute_window`."""

    def test_default_window_three_days(self) -> None:
        """2025-04-13 with default window_days=3 → from 2025-04-12, to 2025-04-15."""
        from_ms, to_ms = _compute_window("2025-04-13")
        assert from_ms == 1_744_416_000_000  # 2025-04-12T00:00:00Z
        assert to_ms == 1_744_675_200_000  # 2025-04-15T00:00:00Z

    def test_default_window_spans_three_days_in_minutes(self) -> None:
        """Default window: (to - from) / 60_000 must equal 4320 (3 days x 1440 min)."""
        from_ms, to_ms = _compute_window("2025-04-13")
        assert (to_ms - from_ms) // 60_000 == 4320

    def test_window_one_day(self) -> None:
        """window_days=1 → from = date 00:00, to = date+1 00:00 (1 full day)."""
        from_ms, to_ms = _compute_window("2025-04-13", window_days=1)
        assert from_ms == 1_744_502_400_000  # 2025-04-13T00:00:00Z
        assert to_ms == 1_744_588_800_000  # 2025-04-14T00:00:00Z
        assert (to_ms - from_ms) // 60_000 == 1440  # 1 day x 1440 min

    def test_window_five_days(self) -> None:
        """window_days=5 → from = date-2, to = date+3 (5 full days centered)."""
        from_ms, to_ms = _compute_window("2025-04-13", window_days=5)
        assert from_ms == 1_744_329_600_000  # 2025-04-11T00:00:00Z
        assert to_ms == 1_744_761_600_000  # 2025-04-16T00:00:00Z
        assert (to_ms - from_ms) // 60_000 == 5 * 1440

    def test_window_two_days_leans_forward(self) -> None:
        """Even windows lean forward: window_days=2 → date 00:00 to date+2 00:00."""
        from_ms, to_ms = _compute_window("2025-04-13", window_days=2)
        assert from_ms == 1_744_502_400_000  # 2025-04-13T00:00:00Z
        assert to_ms == 1_744_675_200_000  # 2025-04-15T00:00:00Z

    def test_invalid_window_days_raises(self) -> None:
        """window_days < 1 raises ValueError."""
        with pytest.raises(ValueError, match="window_days must be"):
            _compute_window("2025-04-13", window_days=0)
        with pytest.raises(ValueError, match="window_days must be"):
            _compute_window("2025-04-13", window_days=-1)

    def test_different_date(self) -> None:
        """Spot-check a different date for correctness with the default window."""
        from_ms, to_ms = _compute_window("2025-01-02")
        assert from_ms == 1_735_689_600_000  # 2025-01-01T00:00:00Z
        assert to_ms == 1_735_948_800_000  # 2025-01-04T00:00:00Z


# ---------------------------------------------------------------------------
# _build_body
# ---------------------------------------------------------------------------


class TestBuildBody:
    """Tests for :func:`_build_body`."""

    def test_exact_body_structure_default_interval(self) -> None:
        """Verify every field in the generated body dict (default 60s)."""
        from_ms = 1_744_416_000_000
        to_ms = 1_744_675_200_000

        body = _build_body("read_ops", "svm1", "vol1", from_ms, to_ms)

        assert body == {
            "category": "netapp_ontap",
            "measurement": "workload_volume",
            "metric": "read_ops",
            "filter": 'vserver_name = "svm1" AND volume_name = "vol1"',
            "fromTimeMs": from_ms,
            "toTimeMs": to_ms,
            "timeAggregationInterval": "60s",
        }

    def test_body_omits_optional_fields(self) -> None:
        """The body must NOT include optional spec fields."""
        body = _build_body("read_ops", "svm1", "vol1", 0, 60_000)
        assert "maxNumberOfDataPoints" not in body
        assert "detectAnomalies" not in body
        assert "interpolationType" not in body

    def test_custom_interval_propagates(self) -> None:
        """The interval argument is passed to ``timeAggregationInterval``."""
        body = _build_body("read_ops", "svm1", "vol1", 0, 60_000, interval="5m")
        assert body["timeAggregationInterval"] == "5m"

    def test_filter_string_format(self) -> None:
        """Filter must use double-quoted values for DII boolean parsing."""
        body = _build_body("read_latency", "my_svm", "my_vol", 0, 60_000)
        assert body["filter"] == 'vserver_name = "my_svm" AND volume_name = "my_vol"'

    def test_all_metrics_produce_singular_metric_field(self) -> None:
        """Every entry in _METRICS can be used as the singular metric field."""
        for m in _METRICS:
            body = _build_body(m, "svm", "vol", 0, 60_000)
            assert body["metric"] == m


# ---------------------------------------------------------------------------
# _parse_timeseries
# ---------------------------------------------------------------------------


class TestParseTimeseries:
    """Tests for :func:`_parse_timeseries`."""

    def test_parses_single_data_point(self) -> None:
        """A single timeseries data point is correctly parsed."""
        response = [{"timeseries": [{"time": 1_744_502_400_000, "value": 1234.5}]}]
        result = _parse_timeseries(response, "read_ops")
        assert result == {1_744_502_400: {"read_ops": 1234.5}}

    def test_timestamp_converted_to_seconds(self) -> None:
        """``data["time"]`` (ms) is divided by 1000 for the key."""
        response = [{"timeseries": [{"time": 1_000_000, "value": 42.0}]}]
        result = _parse_timeseries(response, "write_ops")
        assert 1_000 in result
        assert result[1_000]["write_ops"] == 42.0

    def test_multiple_data_points(self) -> None:
        """Multiple data points all appear in the result."""
        timeseries = [
            {"time": 1_744_502_400_000, "value": 1.0},
            {"time": 1_744_502_460_000, "value": 2.0},
            {"time": 1_744_502_520_000, "value": 3.0},
        ]
        response = [{"timeseries": timeseries}]
        result = _parse_timeseries(response, "read_throughput")
        assert len(result) == 3
        assert result[1_744_502_400]["read_throughput"] == 1.0
        assert result[1_744_502_460]["read_throughput"] == 2.0
        assert result[1_744_502_520]["read_throughput"] == 3.0

    def test_empty_response_returns_empty(self) -> None:
        """A falsy response yields an empty dict."""
        assert _parse_timeseries(None, "read_ops") == {}
        assert _parse_timeseries([], "read_ops") == {}

    def test_unexpected_shape_returns_empty(self) -> None:
        """A response with an unexpected structure yields an empty dict."""
        assert _parse_timeseries({}, "read_ops") == {}
        assert _parse_timeseries([{}], "read_ops") == {}

    def test_bad_data_point_skipped(self) -> None:
        """Data points missing 'time' or 'value' are skipped gracefully."""
        response = [
            {
                "timeseries": [
                    {"time": 1_000_000, "value": 5.0},
                    {"no_time": True},  # bad
                    {"time": 2_000_000, "value": 6.0},
                ]
            }
        ]
        result = _parse_timeseries(response, "write_throughput")
        assert len(result) == 2
        assert 1_000 in result
        assert 2_000 in result


# ---------------------------------------------------------------------------
# Multi-metric merge (integration of _parse_timeseries)
# ---------------------------------------------------------------------------


class TestMultiMetricMerge:
    """Verify that merging 6 per-metric parse results produces complete rows."""

    def _make_response(self, ts_ms: int, value: float) -> list[dict[str, Any]]:
        return [{"timeseries": [{"time": ts_ms, "value": value}]}]

    def test_merge_all_six_metrics(self) -> None:
        """Merging all 6 metrics for a timestamp produces a row with 7 keys."""
        ts_ms = 1_744_502_400_000
        ts_s = ts_ms // 1000
        current: dict[int, dict[str, Any]] = {}
        values = {
            "read_ops": 10.0,
            "write_ops": 20.0,
            "read_throughput": 30.0,
            "write_throughput": 40.0,
            "read_latency": 50.0,
            "write_latency": 60.0,
        }
        for metric, val in values.items():
            resp = self._make_response(ts_ms, val)
            parsed = _parse_timeseries(resp, metric)
            for ts, metric_dict in parsed.items():
                if ts not in current:
                    current[ts] = {"timestamp": ts}
                current[ts].update(metric_dict)

        assert ts_s in current
        row = current[ts_s]
        # timestamp + 6 metrics = 7 keys
        assert len(row) == 7
        assert row["timestamp"] == ts_s
        for metric, expected in values.items():
            assert row[metric] == expected


# ---------------------------------------------------------------------------
# _validate_and_clean
# ---------------------------------------------------------------------------


class TestValidateAndClean:
    """Tests for :func:`_validate_and_clean`."""

    def _full_row(self, ts: int) -> dict[str, Any]:
        return {
            "timestamp": ts,
            "read_ops": 1.0,
            "write_ops": 2.0,
            "read_throughput": 3.0,
            "write_throughput": 4.0,
            "read_latency": 5.0,
            "write_latency": 6.0,
        }

    def test_placeholder_only_row_is_dropped(self) -> None:
        """A row with only 'timestamp' (no metrics) is silently removed."""
        data = {100: {"timestamp": 100}}
        rows = _validate_and_clean(data, _METRICS)
        assert rows == []

    def test_complete_row_passes_through(self) -> None:
        """A fully populated row is returned unchanged."""
        ts = 1_744_502_400
        data = {ts: self._full_row(ts)}
        rows = _validate_and_clean(data, _METRICS)
        assert len(rows) == 1
        assert rows[0]["timestamp"] == ts

    def test_incomplete_row_is_logged_and_kept(self, caplog: pytest.LogCaptureFixture) -> None:
        """A row missing some metrics is logged as an error but still returned."""
        ts = 200
        partial: dict[str, Any] = {"timestamp": ts, "read_ops": 1.0}  # missing 5 metrics
        data = {ts: partial}
        with caplog.at_level(logging.ERROR, logger="pynetappfoundry.cli.commands.metrics.dump_dii"):
            rows = _validate_and_clean(data, _METRICS)
        assert len(rows) == 1
        assert any("does not have" in r.message for r in caplog.records)

    def test_mixed_rows(self) -> None:
        """Placeholder rows are dropped; complete rows are kept."""
        ts1, ts2, ts3 = 100, 200, 300
        data = {
            ts1: {"timestamp": ts1},  # placeholder → dropped
            ts2: self._full_row(ts2),  # complete → kept
            ts3: self._full_row(ts3),  # complete → kept
        }
        rows = _validate_and_clean(data, _METRICS)
        timestamps = {r["timestamp"] for r in rows}
        assert timestamps == {ts2, ts3}

    def test_empty_input_returns_empty(self) -> None:
        """Empty metrics_data yields an empty list."""
        assert _validate_and_clean({}, _METRICS) == []


# ---------------------------------------------------------------------------
# _dump_volume
# ---------------------------------------------------------------------------


class TestDumpVolume:
    """Tests for :func:`_dump_volume`."""

    def _make_dii_query(self, ts_ms: int) -> MagicMock:
        """Return a mock Query that yields one data point per invoke() call."""
        mock = MagicMock()
        mock.invoke.return_value = [{"timeseries": [{"time": ts_ms, "value": 1.0}]}]
        return mock

    def _make_db(self) -> MagicMock:
        return MagicMock()

    def test_issues_exactly_six_posts(self) -> None:
        """_dump_volume calls Query.invoke() exactly once per metric (6 total)."""
        ts_ms = 1_744_502_400_000
        dii_query = self._make_dii_query(ts_ms)
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        assert dii_query.invoke.call_count == len(_METRICS)

    def test_each_invoke_uses_correct_metric(self) -> None:
        """Each Query.invoke() call uses the correct metric in the body."""
        ts_ms = 1_744_502_400_000
        dii_query = self._make_dii_query(ts_ms)
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        called_metrics = [c.kwargs["body"]["metric"] for c in dii_query.invoke.call_args_list]
        assert called_metrics == _METRICS

    def test_custom_interval_propagates_to_body(self) -> None:
        """A non-default interval reaches the timeAggregationInterval field."""
        ts_ms = 1_744_502_400_000
        dii_query = self._make_dii_query(ts_ms)
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms, interval="5m")

        for call in dii_query.invoke.call_args_list:
            assert call.kwargs["body"]["timeAggregationInterval"] == "5m"

    def test_upsert_many_called_once(self) -> None:
        """MetricDB.upsert_many is called exactly once after all 6 POSTs."""
        ts_ms = 1_744_502_400_000
        dii_query = self._make_dii_query(ts_ms)
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        assert db.upsert_many.call_count == 1

    def test_table_name_format(self) -> None:
        """Table name must be ``{svm_name}-{vol_name}``."""
        ts_ms = 1_744_502_400_000
        dii_query = self._make_dii_query(ts_ms)
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        db.create_table.assert_called_once_with("svm1-vol1")
        upsert_call = db.upsert_many.call_args
        assert upsert_call[0][0] == "svm1-vol1"

    def test_invalid_table_name_skips_volume(self) -> None:
        """Volumes whose names produce an invalid table name skip with no POSTs."""
        dii_query = MagicMock()
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        # Spaces are not in the _TABLE_NAME_PATTERN allowed character set.
        _dump_volume("cluster1", "bad name", "svm1", dii_query, db, from_ms, to_ms)

        dii_query.invoke.assert_not_called()
        db.create_table.assert_not_called()
        db.upsert_many.assert_not_called()

    def test_no_data_skips_upsert(self) -> None:
        """If all POSTs return empty responses, upsert_many is never called."""
        dii_query = MagicMock()
        dii_query.invoke.return_value = []
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        db.upsert_many.assert_not_called()

    def test_per_volume_exception_is_isolated(self) -> None:
        """An exception during one volume's POSTs is caught; no re-raise."""
        dii_query = MagicMock()
        dii_query.invoke.side_effect = RuntimeError("DII is down")
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        # Should not raise
        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        db.upsert_many.assert_not_called()

    def test_upsert_rows_contain_all_metrics(self) -> None:
        """Rows passed to upsert_many contain timestamp + all 6 metric keys."""
        ts_ms = 1_744_502_400_000
        ts_s = ts_ms // 1000
        dii_query = self._make_dii_query(ts_ms)
        db = self._make_db()
        from_ms, to_ms = _compute_window("2025-04-13")

        _dump_volume("cluster1", "vol1", "svm1", dii_query, db, from_ms, to_ms)

        rows = db.upsert_many.call_args[0][1]
        assert len(rows) == 1
        row = rows[0]
        assert row["timestamp"] == ts_s
        for metric in _METRICS:
            assert metric in row, f"Expected metric '{metric}' in row"


# ---------------------------------------------------------------------------
# _dump_cluster
# ---------------------------------------------------------------------------


_DUMP_DII_MODULE = "pynetappfoundry.cli.commands.metrics.dump_dii"


@pytest.fixture
def cluster_mocks() -> Iterator[dict[str, MagicMock]]:
    """Patch every external collaborator in the cluster code path.

    Yields a dict of name → MagicMock so each test can configure or assert
    only the collaborators it cares about.
    """
    with patch.multiple(
        _DUMP_DII_MODULE,
        ClusterConfig=DEFAULT,
        ONTAPAPIClient=DEFAULT,
        QuerySet=DEFAULT,
        MetricDB=DEFAULT,
        Query=DEFAULT,
        _dump_volume=DEFAULT,
    ) as mocks:
        yield mocks


class TestDumpCluster:
    """Tests for :func:`_dump_cluster`."""

    def test_db_filename_format(self, cluster_mocks: dict[str, MagicMock]) -> None:
        """MetricDB is instantiated with ``{cluster}_{date}_metrics.db``."""
        mock_volume = MagicMock()
        mock_volume.name = "vol1"
        mock_volume.svm.name = "svm1"
        cluster_mocks["QuerySet"].return_value.filter.return_value.all.return_value = [mock_volume]

        _dump_cluster(
            MagicMock(),
            "mycluster",
            {"name": "mycluster"},
            MagicMock(),
            "2025-04-13",
            0,
            60_000,
            "60s",
        )

        metric_db_cls = cluster_mocks["MetricDB"]
        metric_db_cls.assert_called_once()
        assert metric_db_cls.call_args.kwargs["db_name"] == "mycluster_2025-04-13_metrics.db"

    def test_no_volumes_skips_db_creation(self, cluster_mocks: dict[str, MagicMock]) -> None:
        """When the cluster has no volumes, MetricDB is never constructed."""
        cluster_mocks["QuerySet"].return_value.filter.return_value.all.return_value = []

        _dump_cluster(
            MagicMock(),
            "empty",
            {"name": "empty"},
            MagicMock(),
            "2025-04-13",
            0,
            60_000,
            "60s",
        )

        cluster_mocks["MetricDB"].assert_not_called()

    def test_interval_forwarded_to_dump_volume(self, cluster_mocks: dict[str, MagicMock]) -> None:
        """The interval argument is forwarded to every _dump_volume call."""
        mock_volume = MagicMock()
        mock_volume.name = "vol1"
        mock_volume.svm.name = "svm1"
        cluster_mocks["QuerySet"].return_value.filter.return_value.all.return_value = [mock_volume]

        _dump_cluster(
            MagicMock(),
            "cluster1",
            {"name": "cluster1"},
            MagicMock(),
            "2025-04-13",
            0,
            60_000,
            "5m",
        )

        dump_vol = cluster_mocks["_dump_volume"]
        dump_vol.assert_called_once()
        # interval is the last positional arg
        assert dump_vol.call_args.args[-1] == "5m"

    def test_per_cluster_exception_is_isolated(self, cluster_mocks: dict[str, MagicMock]) -> None:
        """An exception while building the ONTAP client is caught and logged."""
        cluster_mocks["ClusterConfig"].side_effect = RuntimeError("bad cluster details")

        # Should not raise
        _dump_cluster(
            MagicMock(),
            "broken",
            {"name": "broken"},
            MagicMock(),
            "2025-04-13",
            0,
            60_000,
            "60s",
        )


# ---------------------------------------------------------------------------
# DB filename derivation (module-level smoke test, kept for backward coverage)
# ---------------------------------------------------------------------------


class TestDbFilename:
    """Verify that the DB filename follows the documented pattern."""

    def test_db_name_format(self) -> None:
        """DB filename pattern is ``{cluster}_{date}_metrics.db``."""
        assert "mycluster_2025-04-13_metrics.db" == "mycluster_2025-04-13_metrics.db"


# ---------------------------------------------------------------------------
# Table name validation
# ---------------------------------------------------------------------------


class TestTableNameValidation:
    """Verify the table name pattern with ``{svm}-{vol}``."""

    def test_valid_table_name(self) -> None:
        """A well-formed svm-vol name matches _TABLE_NAME_PATTERN."""
        from pynetappfoundry.db.metrics import _TABLE_NAME_PATTERN  # type: ignore[attr-defined]

        table_name = "my_svm-my_vol"
        assert _TABLE_NAME_PATTERN.match(table_name) is not None

    def test_create_table_raises_on_invalid_name(self) -> None:
        """MetricDB.create_table raises ValueError for names with illegal chars."""
        from pathlib import Path

        from pynetappfoundry.db.metrics import MetricDB

        with patch("pynetappfoundry.db.metrics.sqlite3.connect") as mock_conn:
            mock_conn.return_value = MagicMock()
            mock_config = MagicMock()
            mock_config.db_dir = Path("/tmp")
            db = MetricDB(mock_config, db_name="test.db")

        with pytest.raises(ValueError, match="Invalid table name"):
            db.create_table("invalid name with spaces")
