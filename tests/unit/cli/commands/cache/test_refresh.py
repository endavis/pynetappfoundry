"""Tests for cache refresh CLI command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.commands.cache.refresh import VerboseProgressDisplay
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

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_logger")
    def test_refresh_verbose_flag(
        self,
        mock_setup_logger: MagicMock,
        mock_db_class: MagicMock,
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

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_logger")
    def test_refresh_always_logs_to_file(
        self,
        mock_setup_logger: MagicMock,
        mock_db_class: MagicMock,
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

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
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

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_aws_sso_config_passed_to_collector(
        self,
        mock_db_class: MagicMock,
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

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    def test_aws_sso_config_none_when_not_configured(
        self,
        mock_db_class: MagicMock,
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
