"""Tests for AiqumCacheDB (#1055)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.aiqum_collector import AiqumSnapshot
from pynetappfoundry.cache.aiqum_db import AiqumCacheDB


def _snap(
    instance: str = "aiq1",
    records: dict[str, list[dict[str, Any]]] | None = None,
    cached_at: datetime | None = None,
) -> AiqumSnapshot:
    return AiqumSnapshot(
        instance=instance,
        cached_at=cached_at or datetime.now(UTC),
        records=records
        if records is not None
        else {
            "AiqumVolume": [
                {"key": "k1", "name": "vol1", "svm": {"name": "vs1"}, "online": True, "note": None},
                {"key": "k2", "name": "vol2", "svm": {"name": "vs2"}, "online": False, "size": 5},
            ]
        },
    )


@pytest.fixture
def db(tmp_path: Path) -> Iterator[AiqumCacheDB]:
    with AiqumCacheDB(db_path=tmp_path / "aiqum_cache.db") as database:
        yield database


def test_requires_path_or_config() -> None:
    with pytest.raises(ValueError, match="db_path or config"):
        AiqumCacheDB()


def test_config_path(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    with AiqumCacheDB(config=config) as database:
        assert database.db_path == tmp_path / ".cache" / "aiqum_cache.db"
    assert (tmp_path / ".cache" / "aiqum_cache.db").exists()


def test_file_uri(tmp_path: Path) -> None:
    uri = f"file:{tmp_path / 'uri.db'}?mode=rwc"
    with AiqumCacheDB(db_path=uri) as database:
        database.set("aiq1", _snap())
        assert database.is_collected("aiq1", "AiqumVolume")


def test_schema_and_version(db: AiqumCacheDB) -> None:
    tables = {
        r["name"]
        for r in db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    assert {"aiqum_collections", "aiqum_records", "_schema_version"} <= tables
    assert AiqumCacheDB.SCHEMA_VERSION == 1
    assert db.conn.execute("SELECT version FROM _schema_version").fetchone()[0] == 1


def test_round_trip(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    records = db.query_records("aiq1", "AiqumVolume", {})
    assert [r["key"] for r in records] == ["k1", "k2"]
    assert records[0]["svm"] == {"name": "vs1"}


def test_record_key_stored(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    keys = [r[0] for r in db.conn.execute("SELECT record_key FROM aiqum_records ORDER BY _row_id")]
    assert keys == ["k1", "k2"]


def test_dotted_filter(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    assert [r["key"] for r in db.query_records("aiq1", "AiqumVolume", {"svm.name": "vs2"})] == [
        "k2"
    ]


def test_bool_and_int_filters(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    assert [r["key"] for r in db.query_records("aiq1", "AiqumVolume", {"online": True})] == ["k1"]
    assert [r["key"] for r in db.query_records("aiq1", "AiqumVolume", {"online": False})] == ["k2"]
    assert [r["key"] for r in db.query_records("aiq1", "AiqumVolume", {"size": 5})] == ["k2"]


def test_none_filter_matches_null_or_missing(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    assert [r["key"] for r in db.query_records("aiq1", "AiqumVolume", {"note": None})] == [
        "k1",
        "k2",
    ]


def test_combined_filters_are_anded(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    assert db.query_records("aiq1", "AiqumVolume", {"name": "vol1", "svm.name": "vs2"}) == []


@pytest.mark.parametrize("value", [{"a": 1}, ["x"]])
def test_non_scalar_value_rejected(db: AiqumCacheDB, value: Any) -> None:
    with pytest.raises(ValueError, match="scalar"):
        db.query_records("aiq1", "AiqumVolume", {"name": value})


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ('name"; DROP TABLE aiqum_records; --', "vol1"),
        ("name", "x' OR '1'='1"),
        ("name", "vol1'); DROP TABLE aiqum_records; --"),
        ("$.name", "vol1"),
    ],
)
def test_injection_shaped_input_matches_nothing(db: AiqumCacheDB, key: str, value: str) -> None:
    db.set("aiq1", _snap())
    assert db.query_records("aiq1", "AiqumVolume", {key: value}) == []
    assert len(db.query_records("aiq1", "AiqumVolume", {})) == 2


def test_second_set_replaces_first(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    db.set("aiq1", _snap(records={"AiqumVolume": [{"key": "k9", "name": "new"}]}))
    assert [r["key"] for r in db.query_records("aiq1", "AiqumVolume", {})] == ["k9"]


def test_set_keeps_other_mappings(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    db.set("aiq1", _snap(records={"AiqumSvm": [{"key": "s1"}]}))
    assert len(db.query_records("aiq1", "AiqumVolume", {})) == 2
    assert db.is_collected("aiq1", "AiqumSvm")


def test_empty_collection_is_collected(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap(records={"AiqumVolume": []}))
    assert db.is_collected("aiq1", "AiqumVolume")
    assert db.query_records("aiq1", "AiqumVolume", {}) == []


def test_instance_isolation(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    db.set("aiq2", _snap(records={"AiqumVolume": [{"key": "z"}]}))
    assert len(db.query_records("aiq1", "AiqumVolume", {})) == 2
    assert [r["key"] for r in db.query_records("aiq2", "AiqumVolume", {})] == ["z"]
    assert db.list_instances() == ["aiq1", "aiq2"]
    assert not db.is_collected("aiq3", "AiqumVolume")


def test_clear_instance_and_all(db: AiqumCacheDB) -> None:
    db.set("aiq1", _snap())
    db.set("aiq2", _snap())
    assert db.clear("aiq1") == 2
    assert db.list_instances() == ["aiq2"]
    assert db.clear() == 2
    assert db.list_instances() == []


def test_is_stale(db: AiqumCacheDB) -> None:
    assert db.is_stale("aiq1") is None
    db.set("aiq1", _snap())
    assert db.is_stale("aiq1") is False
    db.set("aiq1", _snap(cached_at=datetime.now(UTC) - timedelta(days=40)))
    assert db.is_stale("aiq1") is True
    assert db.is_stale("aiq1", ttl_days=60) is False


def test_list_collections_sorted_and_filtered(db: AiqumCacheDB) -> None:
    db.set("aiq2", _snap("aiq2"))
    db.set("aiq1", _snap("aiq1"))
    rows = db.list_collections()
    assert [(r["instance"], r["mapping"]) for r in rows] == [
        (r["instance"], r["mapping"])
        for r in sorted(rows, key=lambda r: (r["instance"], r["mapping"]))
    ]
    assert {r["instance"] for r in rows} == {"aiq1", "aiq2"}
    only = db.list_collections("aiq1")
    assert only and {r["instance"] for r in only} == {"aiq1"}
    assert set(only[0]) == {"instance", "mapping", "cached_at"}


def test_list_collections_empty(db: AiqumCacheDB) -> None:
    assert db.list_collections() == []
    assert db.list_collections("aiq1") == []
