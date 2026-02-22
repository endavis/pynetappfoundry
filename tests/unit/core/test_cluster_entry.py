"""Tests for ClusterEntry class."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.core.cluster_entry import ClusterEntry


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Sample TOML config data for a cluster."""
    return {
        "name": "test-cluster",
        "ip": "10.0.0.1",
        "bu": "Engineering",
        "env": "Prod",
        "tags": ["active", "workload"],
    }


@pytest.fixture
def cache_db_path(tmp_path: Path) -> Path:
    """Path to a (non-existent) cache DB file."""
    return tmp_path / ".cache" / "cluster_metadata.db"


@pytest.fixture
def entry(sample_data: dict[str, Any], cache_db_path: Path) -> ClusterEntry:
    """Create a ClusterEntry instance."""
    return ClusterEntry("test-cluster", sample_data, cache_db_path)


class TestDictAccess:
    """Tests for dict-like access on ClusterEntry."""

    def test_getitem(self, entry: ClusterEntry) -> None:
        """Test dict-style access returns correct value."""
        assert entry["ip"] == "10.0.0.1"
        assert entry["name"] == "test-cluster"

    def test_getitem_missing_raises_keyerror(self, entry: ClusterEntry) -> None:
        """Test missing key raises KeyError."""
        with pytest.raises(KeyError, match="missing"):
            entry["missing"]

    def test_setitem(self, entry: ClusterEntry) -> None:
        """Test setting a key via dict interface."""
        entry["new_key"] = "new_value"
        assert entry["new_key"] == "new_value"

    def test_delitem(self, entry: ClusterEntry) -> None:
        """Test deleting a key via dict interface."""
        entry["temp"] = "value"
        del entry["temp"]
        assert "temp" not in entry

    def test_contains(self, entry: ClusterEntry) -> None:
        """Test 'in' operator."""
        assert "ip" in entry
        assert "missing" not in entry

    def test_get_with_default(self, entry: ClusterEntry) -> None:
        """Test get() with default value."""
        assert entry.get("ip") == "10.0.0.1"
        assert entry.get("missing") is None
        assert entry.get("missing", "default") == "default"

    def test_keys(self, entry: ClusterEntry) -> None:
        """Test keys() returns underlying dict keys."""
        assert set(entry.keys()) == {"name", "ip", "bu", "env", "tags"}

    def test_values(self, entry: ClusterEntry) -> None:
        """Test values() returns underlying dict values."""
        values = list(entry.values())
        assert "10.0.0.1" in values
        assert "test-cluster" in values

    def test_items(self, entry: ClusterEntry) -> None:
        """Test items() returns key-value pairs."""
        items = dict(entry.items())
        assert items["ip"] == "10.0.0.1"

    def test_len(self, entry: ClusterEntry) -> None:
        """Test len() returns number of keys."""
        assert len(entry) == 5

    def test_iter(self, entry: ClusterEntry) -> None:
        """Test iterating over entry yields keys."""
        assert set(entry) == {"name", "ip", "bu", "env", "tags"}

    def test_unpacking(self, entry: ClusterEntry) -> None:
        """Test that **entry unpacks the TOML dict."""
        result = dict(**entry)
        assert result["ip"] == "10.0.0.1"
        assert result["name"] == "test-cluster"
        assert len(result) == 5


class TestAttributeAccess:
    """Tests for attribute-style access on ClusterEntry."""

    def test_attribute_access(self, entry: ClusterEntry) -> None:
        """Test attribute access returns value from underlying dict."""
        assert entry.ip == "10.0.0.1"
        assert entry.bu == "Engineering"

    def test_attribute_access_missing_raises(self, entry: ClusterEntry) -> None:
        """Test missing attribute raises AttributeError."""
        with pytest.raises(AttributeError, match="missing"):
            entry.missing  # noqa: B018


class TestLazyLoading:
    """Tests for lazy namespace accessor loading."""

    def test_db_not_opened_at_construction(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """Test that the cache DB is not opened during construction."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        with patch("pynetappfoundry.cache.db.ClusterMetadataDB") as mock_db:
            ClusterEntry("test-cluster", sample_data, cache_path)
            mock_db.assert_not_called()

    def test_ontap_opens_db_on_first_access(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """Test that .ontap opens the DB on first access."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_metadata = MagicMock()
        mock_db_instance = MagicMock()
        mock_db_instance.get.return_value = mock_metadata

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            return_value=mock_db_instance,
        ):
            entry = ClusterEntry("test-cluster", sample_data, cache_path)
            result = entry.ontap
            assert result is mock_metadata
            mock_db_instance.get.assert_called_once_with("test-cluster")
            mock_db_instance.close.assert_called_once()

    def test_ontap_cached_on_second_access(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """Test that second .ontap access uses cached result (single DB open)."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_metadata = MagicMock()
        mock_db_instance = MagicMock()
        mock_db_instance.get.return_value = mock_metadata

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            return_value=mock_db_instance,
        ):
            entry = ClusterEntry("test-cluster", sample_data, cache_path)
            result1 = entry.ontap
            result2 = entry.ontap
            assert result1 is result2
            # DB should only be opened once
            mock_db_instance.get.assert_called_once()

    def test_ontap_returns_none_when_no_cache_file(self, entry: ClusterEntry) -> None:
        """Test that .ontap returns None when cache DB file doesn't exist."""
        assert entry.ontap is None

    def test_ontap_returns_none_on_db_error(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """Test that .ontap returns None when DB open fails."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            side_effect=Exception("DB error"),
        ):
            entry = ClusterEntry("test-cluster", sample_data, cache_path)
            assert entry.ontap is None

    def test_ontap_cloud_returns_metadata(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """Test that .ontap.cloud returns cloud metadata list."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_cloud = MagicMock()
        mock_cloud.provider = "Azure"
        mock_metadata = MagicMock()
        mock_metadata.cloud = [mock_cloud]

        mock_db_instance = MagicMock()
        mock_db_instance.get.return_value = mock_metadata

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            return_value=mock_db_instance,
        ):
            entry = ClusterEntry("test-cluster", sample_data, cache_path)
            assert entry.ontap is not None
            assert entry.ontap.cloud[0].provider == "Azure"


class TestFutureNamespaces:
    """Tests for reserved future namespace accessors."""

    def test_occm_returns_none(self, entry: ClusterEntry) -> None:
        """Test that .occm returns None."""
        assert entry.occm is None

    def test_aiqum_returns_none(self, entry: ClusterEntry) -> None:
        """Test that .aiqum returns None."""
        assert entry.aiqum is None

    def test_dii_returns_none(self, entry: ClusterEntry) -> None:
        """Test that .dii returns None."""
        assert entry.dii is None


class TestRepr:
    """Tests for ClusterEntry repr."""

    def test_repr(self, entry: ClusterEntry) -> None:
        """Test repr includes name and data."""
        r = repr(entry)
        assert "ClusterEntry" in r
        assert "test-cluster" in r
