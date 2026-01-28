"""Tests for cache refresh CLI command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


class TestCacheRefreshCommand:
    """Tests for nf cache refresh command."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir(self, tmp_path: Path) -> Path:
        """Create a mock config directory."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        # Create a minimal settings file
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
timeout = 30.0
"""
        )
        # Create a data file with clusters
        (config_dir / "clusters.toml").write_text(
            """
[settings]
type = "data"

[clusters.test-cluster]
ip = "10.0.0.1"
bu = "Test"
env = "Dev"
"""
        )
        # Create users file
        (config_dir / "users.toml").write_text(
            """
[clusters]
user = "admin"
enc = "cGFzc3dvcmQ="
"""
        )
        return config_dir

    def test_refresh_no_args_shows_error(self, runner: CliRunner, mock_config_dir: Path) -> None:
        """Test that refresh without args shows error."""
        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "refresh"])
        assert result.exit_code != 0
        assert "Specify a cluster name or use --all" in result.output

    def test_refresh_nonexistent_cluster(self, runner: CliRunner, mock_config_dir: Path) -> None:
        """Test refresh with nonexistent cluster."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "refresh", "nonexistent"],
        )
        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_refresh_single_cluster(
        self,
        mock_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test refreshing a single cluster."""
        # Setup mocks
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock(cluster_name="test-cluster")
        mock_collector_class.return_value = mock_collector

        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "refresh", "test-cluster"],
        )

        assert result.exit_code == 0
        assert "Cache refreshed" in result.output
        mock_collector.collect_all.assert_called_once_with("test-cluster")
        mock_db.set.assert_called_once()

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_refresh_all_clusters(
        self,
        mock_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test refreshing all clusters."""
        # Setup mocks
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector

        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "refresh", "--all"],
        )

        assert result.exit_code == 0
        mock_collector.collect_all.assert_called()

    def test_refresh_config_not_found(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test refresh with missing config directory."""
        result = runner.invoke(
            nf,
            ["-c", str(tmp_path / "nonexistent"), "cache", "refresh", "--all"],
        )
        assert result.exit_code != 0
        assert "not found" in result.output
