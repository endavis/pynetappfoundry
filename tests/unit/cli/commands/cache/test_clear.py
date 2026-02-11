"""Tests for cache clear CLI command."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache import CachedClusterMetadata
from pynetappfoundry.cli.main import nf


class TestCacheClearCommand:
    """Tests for nf cache clear command."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir(self, tmp_path: Path) -> Path:
        """Create a mock config directory."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
"""
        )
        return config_dir

    def test_clear_no_args_shows_error(self, runner: CliRunner, mock_config_dir: Path) -> None:
        """Test that clear without args shows error."""
        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "clear"])
        assert result.exit_code != 0
        assert "Specify a cluster name or use --all" in result.output

    @patch("pynetappfoundry.cli.commands.cache.clear.ClusterMetadataDB")
    def test_clear_single_cluster(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test clearing single cluster cache."""
        mock_db = MagicMock()
        mock_db.get.return_value = CachedClusterMetadata(
            cluster_name="test-cluster",
            cached_at=datetime.now(UTC),
        )
        mock_db.clear.return_value = 1
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "clear", "test-cluster", "-f"],
        )

        assert result.exit_code == 0
        assert "Cleared cache" in result.output
        mock_db.clear.assert_called_once_with("test-cluster")

    @patch("pynetappfoundry.cli.commands.cache.clear.ClusterMetadataDB")
    def test_clear_single_cluster_with_confirmation(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test clearing with confirmation prompt."""
        mock_db = MagicMock()
        mock_db.get.return_value = CachedClusterMetadata(
            cluster_name="test-cluster",
            cached_at=datetime.now(UTC),
        )
        mock_db.clear.return_value = 1
        mock_db_class.return_value = mock_db

        # Confirm yes
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "clear", "test-cluster"],
            input="y\n",
        )

        assert result.exit_code == 0
        assert "Cleared cache" in result.output

    @patch("pynetappfoundry.cli.commands.cache.clear.ClusterMetadataDB")
    def test_clear_cancelled(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test clearing cancelled by user."""
        mock_db = MagicMock()
        mock_db.get.return_value = CachedClusterMetadata(
            cluster_name="test-cluster",
            cached_at=datetime.now(UTC),
        )
        mock_db_class.return_value = mock_db

        # Confirm no
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "clear", "test-cluster"],
            input="n\n",
        )

        assert result.exit_code == 0
        assert "Cancelled" in result.output
        mock_db.clear.assert_not_called()

    @patch("pynetappfoundry.cli.commands.cache.clear.ClusterMetadataDB")
    def test_clear_nonexistent_cluster(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test clearing nonexistent cluster."""
        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "clear", "nonexistent", "-f"],
        )

        assert result.exit_code == 0
        assert "No cached data found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.clear.ClusterMetadataDB")
    def test_clear_all(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test clearing all cached data."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [
            {"cluster_name": "cluster1"},
            {"cluster_name": "cluster2"},
        ]
        mock_db.clear.return_value = 2
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "clear", "--all", "-f"],
        )

        assert result.exit_code == 0
        assert "Cleared cache for 2" in result.output
        mock_db.clear.assert_called_once_with()

    @patch("pynetappfoundry.cli.commands.cache.clear.ClusterMetadataDB")
    def test_clear_all_empty(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test clearing when cache is empty."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "clear", "--all", "-f"],
        )

        assert result.exit_code == 0
        assert "No cached data found" in result.output

    def test_clear_config_not_found(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test clear with missing config directory."""
        result = runner.invoke(
            nf,
            ["-c", str(tmp_path / "nonexistent"), "cache", "clear", "--all"],
        )
        assert result.exit_code != 0
        assert "not found" in result.output
