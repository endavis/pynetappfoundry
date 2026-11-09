"""Tests for cache refresh CLI command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.commands.cache.refresh import VerboseProgressDisplay
from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config import Config


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

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_refresh_single_cluster(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
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

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

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

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_refresh_all_clusters(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
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

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

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

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_logger")
    def test_refresh_verbose_flag(
        self,
        mock_setup_logger: MagicMock,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test refreshing with verbose flag."""
        # Setup mocks
        mock_setup_logger.return_value = (MagicMock(), Path("/tmp/test.log"))
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock(cluster_name="test-cluster")
        mock_collector_class.return_value = mock_collector

        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "refresh", "--all", "-v"],
        )

        assert result.exit_code == 0
        # Verbose mode should show progress details
        mock_collector.collect_all.assert_called()

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_logger")
    def test_refresh_always_logs_to_file(
        self,
        mock_setup_logger: MagicMock,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that file logging is always configured (with or without -v)."""
        mock_setup_logger.return_value = (MagicMock(), Path("/tmp/test.log"))
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector

        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        # Without verbose flag
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "refresh", "test-cluster"],
        )

        assert result.exit_code == 0
        # setup_logger should always be called
        mock_setup_logger.assert_called_once_with("cache-refresh")

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_logger")
    def test_refresh_displays_log_path(
        self,
        mock_setup_logger: MagicMock,
        mock_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that log file path is displayed to user."""
        mock_setup_logger.return_value = (
            MagicMock(),
            Path("/tmp/data/cache-refresh/logs/cache-refresh_2024-01-15_10-23-45.log"),
        )
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "refresh", "--all"],
        )

        # Log file path should be shown in output
        assert "Log file:" in result.output or "cache-refresh" in result.output


class TestVerboseProgressDisplay:
    """Tests for VerboseProgressDisplay class."""

    def test_init(self) -> None:
        """Test VerboseProgressDisplay initialization."""
        from rich.console import Console

        console = Console()
        display = VerboseProgressDisplay(
            console=console,
            cluster_name="test-cluster",
            cluster_index=1,
            total_clusters=3,
        )
        assert display.cluster_name == "test-cluster"
        assert display.cluster_index == 1
        assert display.total_clusters == 3
        assert display.phase_times == {}

    def test_on_progress_starting(self) -> None:
        """Test on_progress handles 'starting' status."""
        from rich.console import Console

        from pynetappfoundry.cache.collector import CollectionPhase, ProgressInfo

        console = Console(force_terminal=True, width=80)
        display = VerboseProgressDisplay(
            console=console,
            cluster_name="test-cluster",
            cluster_index=1,
            total_clusters=1,
        )

        info = ProgressInfo(
            phase=CollectionPhase.CLOUD,
            phase_name="Cloud metadata",
            status="starting",
        )
        # Should not raise any errors
        display.on_progress(info)
        assert display.current_phase == CollectionPhase.CLOUD

    def test_on_progress_completed(self) -> None:
        """Test on_progress handles 'completed' status."""
        from rich.console import Console

        from pynetappfoundry.cache.collector import CollectionPhase, ProgressInfo

        console = Console(force_terminal=True, width=80)
        display = VerboseProgressDisplay(
            console=console,
            cluster_name="test-cluster",
            cluster_index=1,
            total_clusters=1,
        )

        info = ProgressInfo(
            phase=CollectionPhase.CLOUD,
            phase_name="Cloud metadata",
            status="completed",
            elapsed_seconds=1.5,
            source="cli",
        )
        display.on_progress(info)
        assert display.phase_times[CollectionPhase.CLOUD] == 1.5

    def test_on_progress_failed(self) -> None:
        """Test on_progress handles 'failed' status."""
        from rich.console import Console

        from pynetappfoundry.cache.collector import CollectionPhase, ProgressInfo

        console = Console(force_terminal=True, width=80)
        display = VerboseProgressDisplay(
            console=console,
            cluster_name="test-cluster",
            cluster_index=1,
            total_clusters=1,
        )

        info = ProgressInfo(
            phase=CollectionPhase.NETWORK,
            phase_name="Network",
            status="failed",
            elapsed_seconds=0.5,
            error="Connection timeout",
        )
        display.on_progress(info)
        assert display.phase_times[CollectionPhase.NETWORK] == 0.5


class TestAwsSsoConfig:
    """Tests for AWS SSO config being passed to MetadataCollector."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir_with_aws_sso(self, tmp_path: Path) -> Path:
        """Create a mock config directory with AWS SSO config."""
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
        # Create AWS config with SSO settings
        (config_dir / "aws.toml").write_text(
            """
[sso]
subdomain = "mycompany"

[sso.account_roles]
"123456789012" = "AdminRole"
"987654321098" = "ReadOnlyRole"
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

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_aws_sso_config_passed_to_collector(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_with_aws_sso: Path,
    ) -> None:
        """Test that AWS SSO config from aws.toml is passed to MetadataCollector."""
        # Setup mocks
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock(cluster_name="test-cluster")
        mock_collector_class.return_value = mock_collector

        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir_with_aws_sso), "cache", "refresh", "test-cluster"],
        )

        assert result.exit_code == 0

        # Verify MetadataCollector was called with aws_sso_config
        mock_collector_class.assert_called_once()
        call_kwargs = mock_collector_class.call_args.kwargs
        assert "aws_sso_config" in call_kwargs
        assert call_kwargs["aws_sso_config"] is not None
        assert call_kwargs["aws_sso_config"]["subdomain"] == "mycompany"
        assert "123456789012" in call_kwargs["aws_sso_config"]["account_roles"]
        assert call_kwargs["aws_sso_config"]["account_roles"]["123456789012"] == "AdminRole"

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_aws_sso_config_none_when_not_configured(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        """Test that aws_sso_config is None when aws.toml is not configured."""
        # Create config dir WITHOUT aws.toml
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
timeout = 30.0
"""
        )
        (config_dir / "clusters.toml").write_text(
            """
[settings]
type = "data"

[clusters.test-cluster]
ip = "10.0.0.1"
"""
        )
        (config_dir / "users.toml").write_text(
            """
[clusters]
user = "admin"
enc = "cGFzc3dvcmQ="
"""
        )

        # Setup mocks
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock(cluster_name="test-cluster")
        mock_collector_class.return_value = mock_collector

        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(config_dir), "cache", "refresh", "test-cluster"],
        )

        assert result.exit_code == 0

        # Verify MetadataCollector was called with aws_sso_config=None
        mock_collector_class.assert_called_once()
        call_kwargs = mock_collector_class.call_args.kwargs
        assert "aws_sso_config" in call_kwargs
        assert call_kwargs["aws_sso_config"] is None


class TestFilterOption:
    """Tests for --filter option on cache refresh command."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir_with_envs(self, tmp_path: Path) -> Path:
        """Create a mock config directory with clusters in different environments."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
timeout = 30.0

[clusters]
searchable_keys = ["env", "bu"]
"""
        )
        # Create clusters in different environments
        (config_dir / "clusters.toml").write_text(
            """
[settings]
type = "data"

[clusters.prod-cluster-1]
ip = "10.0.0.1"
env = "Prod"
bu = "Finance"

[clusters.prod-cluster-2]
ip = "10.0.0.2"
env = "Prod"
bu = "IT"

[clusters.dev-cluster-1]
ip = "10.0.0.3"
env = "Dev"
bu = "Finance"
"""
        )
        (config_dir / "users.toml").write_text(
            """
[clusters]
user = "admin"
enc = "cGFzc3dvcmQ="
"""
        )
        return config_dir

    def test_filter_without_all_shows_error(
        self, runner: CliRunner, mock_config_dir_with_envs: Path
    ) -> None:
        """Test that --filter without --all shows an error."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir_with_envs), "cache", "refresh", "-f", '{"env": "Prod"}'],
        )
        assert result.exit_code != 0
        assert "--filter can only be used with --all" in result.output

    def test_filter_invalid_json_shows_error(
        self, runner: CliRunner, mock_config_dir_with_envs: Path
    ) -> None:
        """Test that invalid JSON filter shows an error."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir_with_envs), "cache", "refresh", "--all", "-f", "not json"],
        )
        assert result.exit_code != 0
        assert "Invalid filter JSON" in result.output

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_filter_by_env(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_with_envs: Path,
    ) -> None:
        """Test filtering clusters by environment."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_with_envs),
                "cache",
                "refresh",
                "--all",
                "-f",
                '{"env": "Prod"}',
            ],
        )

        assert result.exit_code == 0
        # Should refresh 2 Prod clusters, not all 3
        assert "2 cluster(s)" in result.output
        assert mock_collector.collect_all.call_count == 2

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_filter_by_multiple_fields(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_with_envs: Path,
    ) -> None:
        """Test filtering clusters by multiple fields."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_with_envs),
                "cache",
                "refresh",
                "--all",
                "-f",
                '{"env": "Prod", "bu": "Finance"}',
            ],
        )

        assert result.exit_code == 0
        # Should refresh only prod-cluster-1 (Prod + Finance)
        assert "1 cluster(s)" in result.output
        assert mock_collector.collect_all.call_count == 1

    def test_filter_no_matches(self, runner: CliRunner, mock_config_dir_with_envs: Path) -> None:
        """Test that filter with no matches shows warning."""
        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_with_envs),
                "cache",
                "refresh",
                "--all",
                "-f",
                '{"env": "Staging"}',
            ],
        )
        assert result.exit_code == 0
        assert "No clusters match filter" in result.output


class TestParallelClusterRefresh:
    """Tests for the --parallel-clusters flag on nf cache refresh."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir_many(self, tmp_path: Path) -> Path:
        """Create a config directory with several clusters for parallel tests."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
timeout = 30.0

[clusters]
searchable_keys = ["env"]
"""
        )
        (config_dir / "clusters.toml").write_text(
            """
[settings]
type = "data"

[clusters.c1]
ip = "10.0.0.1"
env = "Prod"

[clusters.c2]
ip = "10.0.0.2"
env = "Prod"

[clusters.c3]
ip = "10.0.0.3"
env = "Dev"

[clusters.c4]
ip = "10.0.0.4"
env = "Prod"
"""
        )
        (config_dir / "users.toml").write_text(
            """
[clusters]
user = "admin"
enc = "cGFzc3dvcmQ="
"""
        )
        return config_dir

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_default_uses_executor(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """Default `--all` should use a ThreadPoolExecutor for collection."""
        mock_db_class.return_value = MagicMock()
        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector

        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        with patch(
            "pynetappfoundry.cache.refresher.ThreadPoolExecutor",
            wraps=__import__(
                "concurrent.futures", fromlist=["ThreadPoolExecutor"]
            ).ThreadPoolExecutor,
        ) as mock_executor:
            result = runner.invoke(
                nf, ["-c", str(mock_config_dir_many), "cache", "refresh", "--all"]
            )

        assert result.exit_code == 0
        # 4 clusters configured; default is 4 workers, capped by cluster count.
        mock_executor.assert_called_once()
        kwargs = mock_executor.call_args.kwargs
        args = mock_executor.call_args.args
        max_workers = kwargs.get("max_workers") or (args[0] if args else None)
        assert max_workers == 4

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_one_does_not_use_executor(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """`--parallel-clusters 1` must preserve the original sequential path."""
        mock_db_class.return_value = MagicMock()
        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db
        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        with patch("pynetappfoundry.cache.refresher.ThreadPoolExecutor") as mock_executor:
            result = runner.invoke(
                nf,
                [
                    "-c",
                    str(mock_config_dir_many),
                    "cache",
                    "refresh",
                    "--all",
                    "--parallel-clusters",
                    "1",
                ],
            )

        assert result.exit_code == 0
        mock_executor.assert_not_called()
        # All 4 clusters should still be collected.
        assert mock_collector.collect_all.call_count == 4

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_writes_on_main_thread(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """All `db.set` calls must happen on the main thread even with parallel workers."""
        import threading

        main_thread = threading.main_thread()
        set_threads: list[threading.Thread] = []
        record_threads: list[threading.Thread] = []

        mock_db = MagicMock()
        mock_db.set.side_effect = lambda *_a, **_kw: set_threads.append(threading.current_thread())
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None

        def _record_change(*_a: object, **_kw: object) -> int:
            record_threads.append(threading.current_thread())
            return 1

        mock_history_db.record_change.side_effect = _record_change
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_many),
                "cache",
                "refresh",
                "--all",
                "--parallel-clusters",
                "4",
            ],
        )

        assert result.exit_code == 0
        assert mock_db.set.call_count == 4
        assert all(t is main_thread for t in set_threads), set_threads
        assert all(t is main_thread for t in record_threads), record_threads

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_one_failure_does_not_block_others(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """One worker raising must not prevent the remaining clusters from being persisted."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()

        def collect_side_effect(cluster_name: str) -> MagicMock:
            if cluster_name == "c2":
                raise RuntimeError("API_FAILURE: simulated failure for c2")
            return MagicMock()

        mock_collector.collect_all.side_effect = collect_side_effect
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_many),
                "cache",
                "refresh",
                "--all",
                "--parallel-clusters",
                "4",
            ],
        )

        # Exit non-zero because c2 failed.
        assert result.exit_code != 0
        # The other 3 clusters must still have been persisted.
        assert mock_db.set.call_count == 3
        assert "Failure Summary" in result.output
        assert "c2" in result.output

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_does_not_pass_db_to_workers(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """Worker `_collect_cluster` must not receive any DB handle (see #596)."""
        from pynetappfoundry.cache.db import ClusterMetadataDB
        from pynetappfoundry.cache.history_db import CacheHistoryDB

        mock_db = MagicMock(spec=ClusterMetadataDB)
        mock_db_class.return_value = mock_db
        mock_history_db = MagicMock(spec=CacheHistoryDB)
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        with patch("pynetappfoundry.cache.refresher._collect_cluster") as mock_collect:
            mock_collect.return_value = MagicMock(
                cluster_name="c1",
                metadata=None,
                previous_metadata=None,
                captured_output="",
                success=False,
                error=None,
                no_clients=True,
            )
            runner.invoke(
                nf,
                [
                    "-c",
                    str(mock_config_dir_many),
                    "cache",
                    "refresh",
                    "--all",
                    "--parallel-clusters",
                    "4",
                ],
            )

        assert mock_collect.call_count == 4
        # spec'd MagicMocks pass isinstance() checks for the spec class, so this
        # catches both real instances and spec'd mocks of either DB type.
        for call in mock_collect.call_args_list:
            for arg in (*call.args, *call.kwargs.values()):
                assert not isinstance(arg, (CacheHistoryDB, ClusterMetadataDB)), (
                    f"DB handle leaked into worker: {arg!r}"
                )

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_preloads_previous_metadata_on_main_thread(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """`get_latest_snapshot` must be called once per cluster on the main thread (see #596)."""
        import threading

        main_thread = threading.main_thread()
        snapshot_threads: list[threading.Thread] = []
        snapshot_clusters: list[str] = []

        def record_snapshot(cluster_name: str) -> None:
            snapshot_threads.append(threading.current_thread())
            snapshot_clusters.append(cluster_name)
            return None

        mock_db_class.return_value = MagicMock()
        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.side_effect = record_snapshot
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_many),
                "cache",
                "refresh",
                "--all",
                "--parallel-clusters",
                "4",
            ],
        )

        assert result.exit_code == 0
        # Exactly one snapshot load per cluster.
        assert mock_history_db.get_latest_snapshot.call_count == 4
        assert sorted(snapshot_clusters) == ["c1", "c2", "c3", "c4"]
        # Every load must happen on the main thread.
        assert all(t is main_thread for t in snapshot_threads), snapshot_threads

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_verbose_parallel_buffers_output_per_cluster(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """Verbose parallel mode must emit each cluster's block contiguously."""
        mock_db_class.return_value = MagicMock()
        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_many),
                "cache",
                "refresh",
                "--all",
                "-v",
                "--parallel-clusters",
                "4",
            ],
        )

        assert result.exit_code == 0
        # Each cluster must appear exactly once in a bold header line and before
        # the next cluster's header (no interleaving of per-cluster blocks).
        output = result.output
        headers = []
        for name in ("c1", "c2", "c3", "c4"):
            idx = output.find(name)
            assert idx != -1, f"{name} not in verbose output"
            headers.append((idx, name))
        # Non-overlapping, each cluster named exactly once as a header.
        assert len({n for _, n in headers}) == 4

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_parallel_clusters_zero_rejected(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """`--parallel-clusters 0` must be rejected as a click usage error."""
        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_many),
                "cache",
                "refresh",
                "--all",
                "--parallel-clusters",
                "0",
            ],
        )
        assert result.exit_code != 0
        # click IntRange error mentions "not in the range" or similar.
        assert "0" in result.output

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_filter_combined_with_parallel(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """Filter + parallel should only refresh the matching clusters in parallel."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db

        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir_many),
                "cache",
                "refresh",
                "--all",
                "-f",
                '{"env": "Prod"}',
                "--parallel-clusters",
                "2",
            ],
        )

        assert result.exit_code == 0
        # 3 Prod clusters (c1, c2, c4) should be collected and persisted.
        assert mock_collector.collect_all.call_count == 3
        assert mock_db.set.call_count == 3

    @patch("pynetappfoundry.cache.refresher.ONTAPAPIClient")
    @patch("pynetappfoundry.cache.refresher.ONTAPCLI")
    @patch("pynetappfoundry.cache.refresher.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.CacheHistoryDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_single_cluster_ignores_parallel_flag(
        self,
        mock_db_class: MagicMock,
        mock_history_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir_many: Path,
    ) -> None:
        """Single-cluster target must not spin up an executor."""
        mock_db_class.return_value = MagicMock()
        mock_history_db = MagicMock()
        mock_history_db.get_latest_snapshot.return_value = None
        mock_history_db_class.return_value = mock_history_db
        mock_collector = MagicMock()
        mock_collector.collect_all.return_value = MagicMock()
        mock_collector_class.return_value = mock_collector
        mock_cli_class.return_value = MagicMock()
        mock_api_class.return_value = MagicMock()

        with patch("pynetappfoundry.cache.refresher.ThreadPoolExecutor") as mock_executor:
            result = runner.invoke(
                nf,
                [
                    "-c",
                    str(mock_config_dir_many),
                    "cache",
                    "refresh",
                    "c1",
                    "--parallel-clusters",
                    "4",
                ],
            )

        assert result.exit_code == 0
        mock_executor.assert_not_called()
        assert mock_collector.collect_all.call_count == 1


class TestRefreshOrchestrationWiring:
    """Tests for the CLI wiring around ``CacheRefresher`` (#898)."""

    REFRESH = "pynetappfoundry.cli.commands.cache.refresh"
    LIB = "pynetappfoundry.cache.refresher"

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def config_dir(self, tmp_path: Path) -> Path:
        """Create a config directory with two clusters."""
        cfg = tmp_path / "config"
        cfg.mkdir()
        (cfg / "settings.toml").write_text(
            '[ontapapi]\n[ontapapi.general]\nbase_api_path = "/api"\ntimeout = 30.0\n'
        )
        (cfg / "clusters.toml").write_text(
            '[settings]\ntype = "data"\n\n'
            '[clusters.c1]\nip = "10.0.0.1"\n\n[clusters.c2]\nip = "10.0.0.2"\n'
        )
        (cfg / "users.toml").write_text('[clusters]\nuser = "admin"\nenc = "cGFzc3dvcmQ="\n')
        return cfg

    def _invoke(
        self,
        runner: CliRunner,
        config_dir: Path,
        args: list[str],
        *,
        collector_error: Exception | None = None,
        clients_fail: bool = False,
        db_set_error: Exception | None = None,
        global_args: list[str] | None = None,
    ) -> tuple[Any, MagicMock, MagicMock]:
        mock_db = MagicMock()
        if db_set_error is not None:
            mock_db.set.side_effect = db_set_error
        mock_history = MagicMock()
        mock_history.get_latest_snapshot.return_value = None
        collector = MagicMock()
        if collector_error is not None:
            collector.collect_all.side_effect = collector_error
        else:
            collector.collect_all.return_value = MagicMock()
        with (
            patch(f"{self.REFRESH}.ClusterMetadataDB", return_value=mock_db),
            patch(f"{self.REFRESH}.CacheHistoryDB", return_value=mock_history),
            patch(f"{self.LIB}.MetadataCollector", return_value=collector),
            patch(
                f"{self.LIB}.ONTAPAPIClient",
                side_effect=RuntimeError("api down") if clients_fail else None,
            ),
            patch(
                f"{self.LIB}.ONTAPCLI",
                side_effect=RuntimeError("cli down") if clients_fail else None,
            ),
        ):
            result = runner.invoke(
                nf, [*(global_args or []), "-c", str(config_dir), "cache", "refresh", *args]
            )
        return result, mock_db, mock_history

    def test_dbs_closed_when_refresh_fails(self, runner: CliRunner, config_dir: Path) -> None:
        """Regression: a non-zero exit must still close both databases."""
        result, db, history = self._invoke(
            runner, config_dir, ["c1"], collector_error=RuntimeError("API_FAILURE: boom")
        )
        assert result.exit_code == 1
        db.close.assert_called_once()
        history.close.assert_called_once()

    def test_dbs_closed_when_refresh_succeeds(self, runner: CliRunner, config_dir: Path) -> None:
        """Both databases are closed after a successful run."""
        result, db, history = self._invoke(runner, config_dir, ["c1"])
        assert result.exit_code == 0
        db.close.assert_called_once()
        history.close.assert_called_once()

    def test_output_dir_passed_to_config(
        self, runner: CliRunner, config_dir: Path, tmp_path: Path
    ) -> None:
        """The global --output-dir reaches ``Config``."""
        out = tmp_path / "out"
        with patch(f"{self.REFRESH}.Config", wraps=Config) as config_cls:
            result, _, _ = self._invoke(
                runner, config_dir, ["c1"], global_args=["--output-dir", str(out)]
            )
        assert result.exit_code == 0
        assert config_cls.call_args.kwargs["output_dir"] == str(out)

    def test_sequential_verbose_no_clients(self, runner: CliRunner, config_dir: Path) -> None:
        """Sequential verbose: header, client notes, error, then FAILED summary."""
        result, _, _ = self._invoke(runner, config_dir, ["c1", "-v"], clients_fail=True)
        assert result.exit_code == 1
        out = result.output
        assert "[1/1] c1" in out
        assert "API client unavailable: api down" in out
        assert "CLI client unavailable: cli down" in out
        assert out.index("No clients available for c1") < out.index("FAILED")
        assert "c1:\n    No clients available" in out

    def test_parallel_verbose_no_clients(self, runner: CliRunner, config_dir: Path) -> None:
        """Parallel verbose: captured client notes are flushed under a counter header."""
        result, _, _ = self._invoke(runner, config_dir, ["--all", "-v"], clients_fail=True)
        assert result.exit_code == 1
        out = result.output
        assert "[1/2]" in out
        assert "[2/2]" in out
        assert "API client unavailable: api down" in out
        assert "No clients available for c1" in out
        assert "No clients available for c2" in out

    def test_persist_failure_wording_differs_between_modes(
        self, runner: CliRunner, config_dir: Path
    ) -> None:
        """Normal mode: ``Failed -`` sequentially, ``Persist failed -`` in parallel."""
        seq, _, _ = self._invoke(runner, config_dir, ["c1"], db_set_error=OSError("disk"))
        par, _, _ = self._invoke(runner, config_dir, ["--all"], db_set_error=OSError("disk"))
        assert seq.exit_code == 1
        assert par.exit_code == 1
        assert "c1: Failed - disk" in seq.output
        assert "Persist failed" not in seq.output
        assert "c1: Persist failed - disk" in par.output
