"""Tests for AzEventsDB."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.db.azevents import AzEventsDB


@pytest.fixture
def mock_config(tmp_path: Path) -> MagicMock:
    """Create a mock config with db_dir."""
    config = MagicMock()
    config.db_dir = tmp_path
    return config


@pytest.fixture
def db(mock_config: MagicMock) -> Iterator[AzEventsDB]:
    """Open an AzEventsDB and close it afterwards."""
    with AzEventsDB(mock_config) as database:
        yield database


def _columns(conn: sqlite3.Connection) -> list[sqlite3.Row | tuple[object, ...]]:
    return conn.execute("PRAGMA table_info(maintenance_events)").fetchall()


class TestInit:
    """Database creation and schema."""

    def test_default_name(self, mock_config: MagicMock, tmp_path: Path) -> None:
        with AzEventsDB(mock_config):
            pass
        assert (tmp_path / "azevents.db").exists()

    def test_custom_name(self, mock_config: MagicMock, tmp_path: Path) -> None:
        with AzEventsDB(mock_config, db_name="custom.db"):
            pass
        assert (tmp_path / "custom.db").exists()
        assert not (tmp_path / "azevents.db").exists()

    def test_schema_version(self, db: AzEventsDB) -> None:
        row = db.conn.execute("SELECT version FROM _schema_version").fetchone()
        assert row["version"] == 2

    def test_columns_in_order(self, db: AzEventsDB) -> None:
        names = [row["name"] for row in _columns(db.conn)]  # type: ignore[call-overload]
        assert names == [n for n, _ in AzEventsDB.V1_COLUMNS + AzEventsDB.V2_COLUMNS]

    def test_primary_key_and_defaults(self, db: AzEventsDB) -> None:
        pks = {row["name"]: row["pk"] for row in _columns(db.conn)}  # type: ignore[call-overload]
        assert pks["event_id"] == 1
        assert pks["cluster"] == 0
        db.upsert_event({"event_id": "e1"})
        row = db.get_event_by_id("e1")
        assert row is not None
        assert row["event_id"] == "e1"
        assert row["cluster"] == "Unknown"
        assert row["node"] == "Unknown"
        assert row["type"] == "Unknown"


class TestUpgrade:
    """Upgrade from a v1 database."""

    def test_upgrade_from_v1(self, mock_config: MagicMock, tmp_path: Path) -> None:
        path = tmp_path / "azevents.db"
        cols = ", ".join(f"{n} {t}" for n, t in AzEventsDB.V1_COLUMNS)
        conn = sqlite3.connect(path)
        try:
            conn.execute(f"CREATE TABLE maintenance_events ({cols})")
            conn.execute("INSERT INTO maintenance_events (event_id, cluster) VALUES ('old', 'c0')")
            conn.commit()
        finally:
            conn.close()

        with AzEventsDB(mock_config) as db:
            version = db.conn.execute("SELECT version FROM _schema_version").fetchone()
            assert version["version"] == 2
            info = {row["name"]: row["type"] for row in _columns(db.conn)}  # type: ignore[call-overload]
            for name, col_type in AzEventsDB.V2_COLUMNS:
                assert info[name] == col_type.split()[0]
            row = db.get_event_by_id("old")
            assert row is not None
            assert row["cluster"] == "c0"
            assert row["cifs_transition_ms"] is None


class TestQueries:
    """Upsert and lookups."""

    def test_upsert_inserts_then_updates(self, db: AzEventsDB) -> None:
        db.upsert_event({"event_id": "e1", "cluster": "c1", "node": "n1"})
        db.upsert_event({"event_id": "e1", "node": "n2"})
        count = db.conn.execute("SELECT COUNT(*) AS n FROM maintenance_events").fetchone()["n"]
        assert count == 1
        row = db.get_event_by_id("e1")
        assert row is not None
        assert row["node"] == "n2"
        assert row["cluster"] == "c1"

    def test_get_event_by_id(self, db: AzEventsDB) -> None:
        db.upsert_event({"event_id": "e1", "cluster": "c1"})
        db.upsert_event({"event_id": "e2", "cluster": "c2"})
        row = db.get_event_by_id("e2")
        assert row is not None
        assert row["cluster"] == "c2"
        assert db.get_event_by_id("missing") is None

    def test_by_cluster_and_node(self, db: AzEventsDB) -> None:
        db.upsert_event({"event_id": "e1", "cluster": "c1", "node": "n1"})
        db.upsert_event({"event_id": "e2", "cluster": "c2", "node": "n2"})
        assert [r["event_id"] for r in db.get_events_by_cluster("c1")] == ["e1"]
        assert [r["event_id"] for r in db.get_events_by_cluster("c2")] == ["e2"]
        assert db.get_events_by_cluster("nope") == []
        assert [r["event_id"] for r in db.get_events_by_node("n2")] == ["e2"]
        assert [r["event_id"] for r in db.get_events_by_node("n1")] == ["e1"]
        assert db.get_events_by_node("nope") == []

    def test_between_datetimes(self, db: AzEventsDB) -> None:
        db.upsert_event({"event_id": "early", "az_maint_started": datetime(2024, 3, 1, 0, 0, 0)})
        db.upsert_event({"event_id": "start", "az_maint_started": datetime(2024, 3, 10, 0, 0, 0)})
        db.upsert_event({"event_id": "mid", "az_maint_started": datetime(2024, 3, 15, 10, 0, 0)})
        db.upsert_event({"event_id": "end", "az_maint_started": datetime(2024, 3, 20, 0, 0, 0)})
        db.upsert_event({"event_id": "late", "az_maint_started": datetime(2024, 4, 1, 0, 0, 0)})
        db.upsert_event({"event_id": "other", "az_maint_complete": datetime(2024, 3, 15, 0, 0, 0)})
        start = datetime(2024, 3, 10, 0, 0, 0)
        end = datetime(2024, 3, 20, 0, 0, 0)

        rows = db.get_events_between_datetimes("az_maint_started", start, end)
        assert sorted(r["event_id"] for r in rows) == ["end", "mid", "start"]

        rows = db.get_events_between_datetimes("az_maint_complete", start, end)
        assert [r["event_id"] for r in rows] == ["other"]

    def test_datetimes_come_back_as_iso_strings(self, db: AzEventsDB) -> None:
        # Documented contract (#1172): datetime columns are stored and returned
        # as ISO-8601 strings; no converters are applied on read.
        db.upsert_event({"event_id": "e1", "az_maint_started": datetime(2024, 3, 15, 10, 0, 0)})
        row = db.get_event_by_id("e1")
        assert row is not None
        assert row["az_maint_started"] == "2024-03-15T10:00:00"

    def test_text_columns_ignore_global_converters(
        self, mock_config: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # A process-global converter for TEXT must never reach this DB (#1172).
        monkeypatch.setitem(sqlite3.converters, "TEXT", lambda b: "converted")
        with AzEventsDB(mock_config) as database:
            database.upsert_event({"event_id": "e1", "az_maint_started": datetime(2024, 3, 15, 10)})
            row = database.get_event_by_id("e1")
        assert row is not None
        assert row["az_maint_started"] == "2024-03-15T10:00:00"
        assert row["event_id"] == "e1"


def test_no_datetime_column_converters_registered() -> None:
    """The module must not register global converters named after its columns (#1172)."""
    skip = {"event_id", "cluster", "node", "type"}
    names = {
        name.upper()
        for name, col_type in AzEventsDB.V1_COLUMNS + AzEventsDB.V2_COLUMNS
        if col_type.split()[0] == "TEXT" and name not in skip
    }
    assert names
    assert not names & set(sqlite3.converters)
