"""Tests for cache show CLI command."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache import CachedClusterMetadata
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cli.main import nf


class TestCacheShowCommand:
    """Tests for nf cache show command."""

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

    @pytest.fixture
    def sample_metadata(self) -> CachedClusterMetadata:
        """Create sample metadata for testing."""
        return CachedClusterMetadata(
            cluster_name="test-cluster",
            cached_at=datetime(2024, 1, 15, 10, 30, 0, tzinfo=UTC),
            cloud=[CloudMetadata(provider="AWS", region="us-east-1")],
        )

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_list_clusters(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test showing list of cached clusters."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [
            {
                "cluster_name": "cluster1",
                "cached_at": "2024-01-15T10:30:00+00:00",
                "cache_version": "1.0",
            },
            {
                "cluster_name": "cluster2",
                "cached_at": "2024-01-14T10:30:00+00:00",
                "cache_version": "1.0",
            },
        ]
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "show"])

        assert result.exit_code == 0
        assert "cluster1" in result.output
        assert "cluster2" in result.output

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_empty_cache(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test showing empty cache."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "show"])

        assert result.exit_code == 0
        assert "No cached clusters" in result.output

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_specific_cluster(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test showing specific cluster."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "show", "test-cluster"])

        assert result.exit_code == 0
        assert "test-cluster" in result.output
        assert "AWS" in result.output

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_nonexistent_cluster(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test showing nonexistent cluster."""
        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        result = runner.invoke(nf, ["-c", str(mock_config_dir), "cache", "show", "nonexistent"])

        assert result.exit_code != 0
        assert "No cached data found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_specific_section(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test showing specific section."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "show", "test-cluster", "-s", "cloud"],
        )

        assert result.exit_code == 0
        assert "cloud" in result.output.lower()

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_json_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test JSON output."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "show", "test-cluster", "--json"],
        )

        assert result.exit_code == 0
        assert '"cluster_name"' in result.output
        assert '"AWS"' in result.output

    def test_show_config_not_found(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test show with missing config directory."""
        result = runner.invoke(
            nf,
            ["-c", str(tmp_path / "nonexistent"), "cache", "show"],
        )
        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_invalid_cluster_name(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test showing invalid cluster name gives user-friendly error."""
        mock_db = MagicMock()
        mock_db.get.side_effect = ValueError("Invalid cluster name")
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "show", "cloud[*].account_id"],
        )

        assert result.exit_code != 0
        assert "Invalid cluster name" in result.output
        # Should suggest using cache query instead
        assert "nf cache query" in result.output

    @patch("pynetappfoundry.cli.commands.cache.show.ClusterMetadataDB")
    def test_show_invalid_cluster_name_no_query_suggestion(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test invalid cluster name without dots doesn't suggest query."""
        mock_db = MagicMock()
        mock_db.get.side_effect = ValueError("Invalid cluster name")
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "show", "invalid@name!"],
        )

        assert result.exit_code != 0
        assert "Invalid cluster name" in result.output
        # Should NOT suggest cache query for names without dots/brackets
        assert "nf cache query" not in result.output
