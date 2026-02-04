"""Tests for cache refresh CLI command."""

from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.commands.cache.refresh import (
    VerboseProgressDisplay,
    cleanup_old_logs,
    setup_file_logging,
)
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
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_file_logging")
    def test_refresh_verbose_flag(
        self,
        mock_setup_logging: MagicMock,
        mock_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test refreshing with verbose flag."""
        # Setup mocks
        mock_setup_logging.return_value = Path("/tmp/test.log")
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
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_file_logging")
    def test_refresh_always_logs_to_file(
        self,
        mock_setup_logging: MagicMock,
        mock_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that file logging is always configured (with or without -v)."""
        mock_setup_logging.return_value = Path("/tmp/test.log")
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
        # setup_file_logging should always be called
        mock_setup_logging.assert_called_once()

    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.refresh.MetadataCollector")
    @patch("pynetappfoundry.cli.commands.cache.refresh.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.refresh.setup_file_logging")
    def test_refresh_displays_log_path(
        self,
        mock_setup_logging: MagicMock,
        mock_db_class: MagicMock,
        mock_collector_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that log file path is displayed to user."""
        mock_setup_logging.return_value = Path("/tmp/cache-refresh-test.log")
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


class TestSetupFileLogging:
    """Tests for file logging setup."""

    @patch("pynetappfoundry.cli.commands.cache.refresh.LOG_DIR", None)
    def test_setup_file_logging_creates_directory(self, tmp_path: Path) -> None:
        """Test that setup creates log directory if it doesn't exist."""
        with (
            patch("pynetappfoundry.cli.commands.cache.refresh.LOG_DIR", tmp_path / "logs"),
            patch("pynetappfoundry.cli.commands.cache.refresh.cleanup_old_logs"),
        ):
            log_file = setup_file_logging()
            assert log_file.parent.exists()
            assert "cache-refresh" in log_file.name

    def test_setup_file_logging_creates_timestamped_file(self, tmp_path: Path) -> None:
        """Test that log files have timestamps in names."""
        with (
            patch("pynetappfoundry.cli.commands.cache.refresh.LOG_DIR", tmp_path / "logs"),
            patch("pynetappfoundry.cli.commands.cache.refresh.cleanup_old_logs"),
        ):
            log_file = setup_file_logging()
            # Should match pattern: cache-refresh-YYYYMMDD-HHMMSS.log
            assert log_file.name.startswith("cache-refresh-")
            assert log_file.suffix == ".log"

    def test_setup_file_logging_configures_handlers(self, tmp_path: Path) -> None:
        """Test that logging handlers are configured."""
        with (
            patch("pynetappfoundry.cli.commands.cache.refresh.LOG_DIR", tmp_path / "logs"),
            patch("pynetappfoundry.cli.commands.cache.refresh.cleanup_old_logs"),
        ):
            log_file = setup_file_logging()
            assert log_file.exists()

            # Cache logger should have a file handler
            cache_logger = logging.getLogger("pynetappfoundry.cache")
            file_handlers = [h for h in cache_logger.handlers if isinstance(h, logging.FileHandler)]
            assert len(file_handlers) > 0

            # Clean up handlers
            for handler in file_handlers:
                cache_logger.removeHandler(handler)
                handler.close()


class TestCleanupOldLogs:
    """Tests for log file cleanup."""

    def test_cleanup_old_logs_keeps_recent_files(self, tmp_path: Path) -> None:
        """Test that recent log files are kept."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        # Create some log files
        for i in range(5):
            (log_dir / f"cache-refresh-2024010{i}-120000.log").write_text("test")

        with (
            patch("pynetappfoundry.cli.commands.cache.refresh.LOG_DIR", log_dir),
            patch("pynetappfoundry.cli.commands.cache.refresh.MAX_LOG_FILES", 10),
        ):
            cleanup_old_logs()

        # All 5 files should still exist (under MAX_LOG_FILES)
        remaining = list(log_dir.glob("cache-refresh-*.log"))
        assert len(remaining) == 5

    def test_cleanup_old_logs_removes_old_files(self, tmp_path: Path) -> None:
        """Test that old log files are removed."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        # Create 15 log files
        for i in range(15):
            (log_dir / f"cache-refresh-2024010{i:02d}-120000.log").write_text("test")

        with (
            patch("pynetappfoundry.cli.commands.cache.refresh.LOG_DIR", log_dir),
            patch("pynetappfoundry.cli.commands.cache.refresh.MAX_LOG_FILES", 10),
        ):
            cleanup_old_logs()

        # Only MAX_LOG_FILES should remain
        remaining = list(log_dir.glob("cache-refresh-*.log"))
        assert len(remaining) == 10

    def test_cleanup_old_logs_nonexistent_directory(self, tmp_path: Path) -> None:
        """Test cleanup handles nonexistent directory gracefully."""
        with patch(
            "pynetappfoundry.cli.commands.cache.refresh.LOG_DIR",
            tmp_path / "nonexistent",
        ):
            # Should not raise any errors
            cleanup_old_logs()


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
