"""Tests for EmsEventsDB."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.db.ems import EmsEventsDB


@pytest.fixture
def mock_config(tmp_path: Path) -> MagicMock:
    """Create a mock config with db_dir."""
    config = MagicMock()
    config.db_dir = tmp_path
    return config


@pytest.fixture
def db(mock_config: MagicMock) -> Iterator[EmsEventsDB]:
    """Open an EmsEventsDB and close it afterwards."""
    with EmsEventsDB(mock_config) as database:
        yield database


class TestInit:
    """Creation and overwrite behavior."""

    def test_default_location(self, mock_config: MagicMock, tmp_path: Path) -> None:
        with EmsEventsDB(mock_config) as db:
            assert db.exists is False
            assert db.overwrite is True
        assert (tmp_path / "emsevents").is_dir()
        assert (tmp_path / "emsevents" / "ems_events.db").exists()

    def test_custom_name(self, mock_config: MagicMock, tmp_path: Path) -> None:
        with EmsEventsDB(mock_config, db_name="other.db"):
            pass
        assert (tmp_path / "emsevents" / "other.db").exists()
        assert not (tmp_path / "emsevents" / "ems_events.db").exists()

    def test_reopen_without_overwrite_keeps_data(self, mock_config: MagicMock) -> None:
        with EmsEventsDB(mock_config) as first:
            first.insert_event({"event_id": "e1", "node": "n1"})
        with EmsEventsDB(mock_config, overwrite=False) as second:
            assert second.exists is True
            assert second.overwrite is False
            assert len(second.get_events_by_node("n1")) == 1

    def test_reopen_with_overwrite_drops_data(self, mock_config: MagicMock) -> None:
        with EmsEventsDB(mock_config) as first:
            first.insert_event({"event_id": "e1", "node": "n1"})
        with EmsEventsDB(mock_config) as second:
            assert second.exists is True
            assert second.get_events_by_node("n1") == []


class TestEvents:
    """Insert and query."""

    def test_defaults(self, db: EmsEventsDB) -> None:
        cols = [row[1] for row in db.conn.execute("PRAGMA table_info(ems_events)").fetchall()]
        assert cols == ["event_id", "cluster", "node", "time", "event", "severity", "message"]
        db.insert_event({"event_id": "e1", "node": "n1", "time": "2024-03-15T10:00:00"})
        rows = db.get_events_by_node("n1")
        assert rows == [
            ("e1", "Unknown", "n1", "2024-03-15T10:00:00", "Unknown", "Unknown", "Unknown")
        ]

    def test_no_dedupe(self, db: EmsEventsDB) -> None:
        db.insert_event({"event_id": "e1", "node": "n1"})
        db.insert_event({"event_id": "e1", "node": "n1"})
        assert len(db.get_events_by_node("n1")) == 2

    def test_by_node(self, db: EmsEventsDB) -> None:
        db.insert_event({"event_id": "e1", "node": "n1"})
        db.insert_event({"event_id": "e2", "node": "n2"})
        assert [r[0] for r in db.get_events_by_node("n2")] == ["e2"]
        assert db.get_events_by_node("nope") == []

    def test_between_datetimes(self, db: EmsEventsDB) -> None:
        # Documented contract (#1172): times are stored and returned as
        # ISO-8601 strings, not datetimes.
        for event_id, when in [
            ("early", datetime(2024, 3, 1)),
            ("start", datetime(2024, 3, 10)),
            ("mid", datetime(2024, 3, 15, 10)),
            ("end", datetime(2024, 3, 20)),
            ("late", datetime(2024, 4, 1)),
        ]:
            db.insert_event({"event_id": event_id, "time": when})
        rows = db.get_events_between_datetimes(datetime(2024, 3, 10), datetime(2024, 3, 20))
        assert sorted(r[0] for r in rows) == ["end", "mid", "start"]
        assert {r[0]: r[3] for r in rows}["mid"] == "2024-03-15T10:00:00"


def test_text_columns_ignore_global_converters(
    mock_config: MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A process-global converter for TEXT must never reach this DB (#1172).
    monkeypatch.setitem(sqlite3.converters, "TEXT", lambda b: "converted")
    with EmsEventsDB(mock_config) as database:
        database.insert_event({"event_id": "e1", "node": "n1", "time": datetime(2024, 3, 15, 10)})
        rows = database.get_events_by_node("n1")
    assert rows[0][3] == "2024-03-15T10:00:00"


def test_time_converter_not_registered() -> None:
    """The module must not register a global "time" converter (#1172)."""
    assert "TIME" not in sqlite3.converters
