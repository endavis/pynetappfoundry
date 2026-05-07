"""Tests for ``pynetappfoundry.cli.commands.metrics.dump_dii`` helpers.

All tests target the pure helper functions; the Click command is not invoked
via CliRunner (consistent with sibling test files in this package tree).
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.metrics.dump_dii import (
    _METRICS,
    _build_body,
    _compute_window,
    _dump_volume,
    _parse_timeseries,
    _validate_and_clean,
)

# ---------------------------------------------------------------------------
# _compute_window
# ---------------------------------------------------------------------------


class TestComputeWindow:
    """Tests for :func:`_compute_window`."""

    def test_exact_millisecond_values(self) -> None:
        """2025-04-13 → from=2025-04-12T00:00:00Z, to=2025-04-15T00:00:00Z."""
        # 2025-04-12T00:00:00Z
        expected_from_ms = 1_744_416_000_000
        # 2025-04-15T00:00:00Z
        expected_to_ms = 1_744_675_200_000

        from_ms, to_ms = _compute_window("2025-04-13")

        assert from_ms == expected_from_ms
        assert to_ms == expected_to_ms

    def test_window_spans_three_days_in_minutes(self) -> None:
        """(to - from) / 60_000 must equal 4320 (3 days x 1440 min)."""
        from_ms, to_ms = _compute_window("2025-04-13")
        assert (to_ms - from_ms) // 60_000 == 4320

    def test_from_is_one_day_before_to_is_two_days_after(self) -> None:
        """Window: date-1 day → date+2 days (3-day span total)."""
        from_ms, to_ms = _compute_window("2025-01-01")
        # 3 days = 3 * 24 * 3600 * 1000 ms
        assert to_ms - from_ms == 3 * 24 * 3600 * 1000

    def test_different_date(self) -> None:
        """Spot-check a different date for correctness."""
        from_ms, to_ms = _compute_window("2025-01-02")
        # from = 2025-01-01T00:00:00Z, to = 2025-01-04T00:00:00Z
        assert from_ms == 1_735_689_600_000
        assert to_ms == 1_735_948_800_000


# ---------------------------------------------------------------------------
# _build_body
# ---------------------------------------------------------------------------


class TestBuildBody:
    """Tests for :func:`_build_body`."""

    def test_exact_body_structure(self) -> None:
        """Verify every field in the generated body dict."""
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
            "maxNumberOfDataPoints": (to_ms - from_ms) // 60_000,
            "detectAnomalies": False,
            "interpolationType": "NONE",
        }

    def test_max_data_points_matches_window(self) -> None:
        """maxNumberOfDataPoints must equal (to - from) // 60_000."""
        from_ms, to_ms = _compute_window("2025-04-13")
        body = _build_body("write_ops", "svm2", "vol2", from_ms, to_ms)
        assert body["maxNumberOfDataPoints"] == (to_ms - from_ms) // 60_000

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
        import logging

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
# DB filename derivation
# ---------------------------------------------------------------------------


class TestDbFilename:
    """Verify that the DB filename follows the documented pattern."""

    def test_db_name_format(self) -> None:
        """MetricDB must be constructed with ``{cluster}_{date}_metrics.db``."""
        cluster_name = "mycluster"
        date = "2025-04-13"
        expected_db_name = f"{cluster_name}_{date}_metrics.db"
        assert expected_db_name == "mycluster_2025-04-13_metrics.db"

    def test_db_name_constructed_in_dump_dii(self) -> None:
        """dump_dii calls MetricDB with the per-cluster-per-date filename."""
        with patch("pynetappfoundry.cli.commands.metrics.dump_dii.MetricDB") as mock_db_cls:
            mock_config = MagicMock()
            date = "2025-04-13"

            from pynetappfoundry.cli.commands.metrics.dump_dii import MetricDB as _MetricDB

            _ = _MetricDB(mock_config, db_name=f"mycluster_{date}_metrics.db")

            expected_db_name = "mycluster_2025-04-13_metrics.db"
            mock_db_cls.assert_called_once_with(mock_config, db_name=expected_db_name)


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
