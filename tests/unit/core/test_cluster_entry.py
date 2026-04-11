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
        mock_db_instance.get_lazy.return_value = mock_metadata

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            return_value=mock_db_instance,
        ):
            entry = ClusterEntry("test-cluster", sample_data, cache_path)
            result = entry.ontap
            assert result is mock_metadata
            mock_db_instance.get_lazy.assert_called_once_with("test-cluster")
            # After fix: success path does NOT close db; shim owns the connection.
            mock_db_instance.close.assert_not_called()

    def test_cache_db_constructed_with_config(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """ClusterMetadataDB is constructed with config= so get_lazy() works.

        Regression for #548: previously the db was constructed without
        ``config=``, causing ``get_lazy()`` to raise ``ValueError``. Also
        verifies the db is NOT closed when a shim is returned, since the
        shim shares the open connection.
        """
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_metadata = MagicMock()
        mock_db_instance = MagicMock()
        mock_db_instance.get_lazy.return_value = mock_metadata
        mock_config = MagicMock()

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            return_value=mock_db_instance,
        ) as mock_db:
            entry = ClusterEntry("test-cluster", sample_data, cache_path, config=mock_config)
            result = entry.ontap
            assert result is mock_metadata
            # Key assertion: BOTH db_path and config must be passed.
            mock_db.assert_called_once_with(db_path=cache_path, config=mock_config)
            # Db must NOT be closed: the shim owns the connection.
            mock_db_instance.close.assert_not_called()

    def test_ontap_cached_on_second_access(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """Test that second .ontap access uses cached result (single DB open)."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_metadata = MagicMock()
        mock_db_instance = MagicMock()
        mock_db_instance.get_lazy.return_value = mock_metadata

        with patch(
            "pynetappfoundry.cache.db.ClusterMetadataDB",
            return_value=mock_db_instance,
        ):
            entry = ClusterEntry("test-cluster", sample_data, cache_path)
            result1 = entry.ontap
            result2 = entry.ontap
            assert result1 is result2
            # DB should only be opened once
            mock_db_instance.get_lazy.assert_called_once()

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
        mock_db_instance.get_lazy.return_value = mock_metadata

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


class TestConfigAwareFetcher:
    """Tests for Config-aware ontap property with live fetcher."""

    def test_ontap_returns_lazy_with_fetcher_when_no_cache_but_config(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """When no cache DB but Config is available, ontap returns fetcher-backed lazy."""
        from pynetappfoundry.cache._lazy import LazyClusterMetadata

        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        # cache_path does NOT exist
        mock_config = MagicMock()
        mock_config.get_user.return_value = ("admin", "pass")

        with patch("pynetappfoundry.cache._fetcher.FieldGroupFetcher") as mock_fetcher_cls:
            mock_fetcher = MagicMock()
            mock_fetcher_cls.return_value = mock_fetcher

            entry = ClusterEntry("test-cluster", sample_data, cache_path, config=mock_config)
            result = entry.ontap

            assert result is not None
            assert isinstance(result, LazyClusterMetadata)
            assert result._fetcher is mock_fetcher

    def test_ontap_returns_none_when_no_cache_and_no_config(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """When no cache DB and no Config, ontap returns None."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        entry = ClusterEntry("test-cluster", sample_data, cache_path)
        assert entry.ontap is None

    def test_ontap_returns_none_when_no_cache_no_ip_but_config(self, tmp_path: Path) -> None:
        """When no cache DB and no IP in config data, ontap returns None."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        data: dict[str, Any] = {"name": "test-cluster"}  # no 'ip' key
        mock_config = MagicMock()
        entry = ClusterEntry("test-cluster", data, cache_path, config=mock_config)
        assert entry.ontap is None

    def test_ontap_attaches_fetcher_when_cache_exists_and_config(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """When cache DB exists and Config available, fetcher is attached to lazy result."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_metadata = MagicMock()
        mock_metadata._fetcher = None
        mock_db_instance = MagicMock()
        mock_db_instance.get_lazy.return_value = mock_metadata

        mock_config = MagicMock()
        mock_config.get_user.return_value = ("admin", "pass")

        with (
            patch(
                "pynetappfoundry.cache.db.ClusterMetadataDB",
                return_value=mock_db_instance,
            ),
            patch("pynetappfoundry.cache._fetcher.FieldGroupFetcher") as mock_fetcher_cls,
        ):
            mock_fetcher = MagicMock()
            mock_fetcher_cls.return_value = mock_fetcher

            entry = ClusterEntry("test-cluster", sample_data, cache_path, config=mock_config)
            result = entry.ontap

            assert result is not None
            assert result is mock_metadata
            assert result._fetcher is mock_fetcher

    def test_config_passed_through_from_config_class(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """ClusterEntry stores the config reference."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        mock_config = MagicMock()
        entry = ClusterEntry("test-cluster", sample_data, cache_path, config=mock_config)
        assert entry._config is mock_config

    def test_config_default_is_none(self, sample_data: dict[str, Any], tmp_path: Path) -> None:
        """ClusterEntry without config kwarg has _config=None."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        entry = ClusterEntry("test-cluster", sample_data, cache_path)
        assert entry._config is None


class TestNoCacheBypass:
    """Tests for the no_cache constructor flag."""

    def test_no_cache_default_false(self, entry: ClusterEntry) -> None:
        """Default constructor leaves _no_cache False."""
        assert entry._no_cache is False

    def test_no_cache_stored(self, sample_data: dict[str, Any], cache_db_path: Path) -> None:
        """no_cache=True is stored on the entry."""
        entry = ClusterEntry("test-cluster", sample_data, cache_db_path, no_cache=True)
        assert entry._no_cache is True

    def test_no_cache_skips_db_even_when_present(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """When no_cache=True, .ontap does not open the cache DB."""
        from pynetappfoundry.cache._lazy import LazyClusterMetadata

        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.touch()

        mock_config = MagicMock()
        mock_config.get_user.return_value = ("admin", "pass")

        with (
            patch("pynetappfoundry.cache.db.ClusterMetadataDB") as mock_db_cls,
            patch("pynetappfoundry.cache._fetcher.FieldGroupFetcher") as mock_fetcher_cls,
        ):
            mock_fetcher = MagicMock()
            mock_fetcher_cls.return_value = mock_fetcher

            entry = ClusterEntry(
                "test-cluster",
                sample_data,
                cache_path,
                config=mock_config,
                no_cache=True,
            )
            result = entry.ontap

            mock_db_cls.assert_not_called()
            assert result is not None
            assert isinstance(result, LazyClusterMetadata)
            assert result._db_path is None
            assert result._fetcher is mock_fetcher

    def test_no_cache_returns_none_without_config(
        self, sample_data: dict[str, Any], tmp_path: Path
    ) -> None:
        """no_cache=True without a Config returns None (no fetcher possible)."""
        cache_path = tmp_path / ".cache" / "cluster_metadata.db"
        entry = ClusterEntry("test-cluster", sample_data, cache_path, no_cache=True)
        assert entry.ontap is None


class TestRepr:
    """Tests for ClusterEntry repr."""

    def test_repr(self, entry: ClusterEntry) -> None:
        """Test repr includes name and data."""
        r = repr(entry)
        assert "ClusterEntry" in r
        assert "test-cluster" in r
