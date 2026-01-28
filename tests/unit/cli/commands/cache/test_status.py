"""Tests for cache status CLI command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


class TestCacheStatusCommand:
    """Tests for nf cache status command."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir(self, tmp_path: Path) -> Path:
        """Create a mock config directory with clusters."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
"""
        )
        (config_dir / "clusters.toml").write_text(
            """
[settings]
type = "data"

[clusters.cluster1]
ip = "10.0.0.1"

[clusters.cluster2]
ip = "10.0.0.2"
"""
        )
        return config_dir

    @patch("pynetappfoundry.cli.commands.cache.status.ClusterMetadataDB")
    def test_status_all_cached(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test status when all clusters are cached."""
        mock_db = MagicMock()
        mock_db.get_status.return_value = [
            {
                "cluster_name": "cluster1",
                "cached_at": "2024-01-15T10:30:00+00:00",
                "cache_version": "1.0",
                "age_days": 5,
                "is_stale": False,
            },
            {
                "cluster_name": "cluster2",
                "cached_at": "2024-01-10T10:30:00+00:00",
                "cache_version": "1.0",
                "age_days": 10,
                "is_stale": False,
            },
        ]
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "status"])

        assert result.exit_code == 0
        assert "cluster1" in result.output
        assert "cluster2" in result.output
        assert "Fresh" in result.output

    @patch("pynetappfoundry.cli.commands.cache.status.ClusterMetadataDB")
    def test_status_with_stale(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test status with stale cache."""
        mock_db = MagicMock()
        mock_db.get_status.return_value = [
            {
                "cluster_name": "cluster1",
                "cached_at": "2023-12-01T10:30:00+00:00",
                "cache_version": "1.0",
                "age_days": 50,
                "is_stale": True,
            },
        ]
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "status"])

        assert result.exit_code == 0
        assert "Stale" in result.output

    @patch("pynetappfoundry.cli.commands.cache.status.ClusterMetadataDB")
    def test_status_missing_clusters(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test status when some clusters are not cached."""
        mock_db = MagicMock()
        mock_db.get_status.return_value = [
            {
                "cluster_name": "cluster1",
                "cached_at": "2024-01-15T10:30:00+00:00",
                "cache_version": "1.0",
                "age_days": 5,
                "is_stale": False,
            },
        ]  # cluster2 is missing
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "status"])

        assert result.exit_code == 0
        assert "cluster1" in result.output
        assert "cluster2" in result.output
        assert "Not cached" in result.output
        assert "Missing cache for" in result.output

    @patch("pynetappfoundry.cli.commands.cache.status.ClusterMetadataDB")
    def test_status_empty_cache(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test status when cache is empty."""
        mock_db = MagicMock()
        mock_db.get_status.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "status"])

        assert result.exit_code == 0
        assert "cluster1" in result.output
        assert "cluster2" in result.output
        assert "Not cached" in result.output

    @patch("pynetappfoundry.cli.commands.cache.status.ClusterMetadataDB")
    def test_status_custom_ttl(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test status with custom TTL."""
        mock_db = MagicMock()
        mock_db.get_status.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "status", "--ttl", "7"])

        assert result.exit_code == 0
        mock_db.get_status.assert_called_once_with(ttl_days=7)

    @patch("pynetappfoundry.cli.commands.cache.status.ClusterMetadataDB")
    def test_status_orphaned_cache(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test status with orphaned cache entries."""
        mock_db = MagicMock()
        mock_db.get_status.return_value = [
            {
                "cluster_name": "cluster1",
                "cached_at": "2024-01-15T10:30:00+00:00",
                "cache_version": "1.0",
                "age_days": 5,
                "is_stale": False,
            },
            {
                "cluster_name": "orphaned-cluster",  # Not in config
                "cached_at": "2024-01-15T10:30:00+00:00",
                "cache_version": "1.0",
                "age_days": 5,
                "is_stale": False,
            },
        ]
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "status"])

        assert result.exit_code == 0
        assert "Orphaned" in result.output
        assert "orphaned-cluster" in result.output

    def test_status_config_not_found(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test status with missing config directory."""
        result = runner.invoke(
            nf,
            ["-c", str(tmp_path / "nonexistent"), "cache", "status"],
        )
        assert result.exit_code != 0
        assert "not found" in result.output
