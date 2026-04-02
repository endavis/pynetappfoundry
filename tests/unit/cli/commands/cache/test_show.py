"""Tests for cache show CLI command."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache import CachedClusterMetadata
from pynetappfoundry.cache.db import all_realtime_attrs
from pynetappfoundry.cli.commands.cache.show import _strip_realtime_fields
from pynetappfoundry.cli.main import nf
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata


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


class TestStripRealtimeFields:
    """Tests for _strip_realtime_fields helper."""

    def test_removes_known_realtime_keys(self) -> None:
        """Realtime keys are stripped from a flat dict."""
        rt = frozenset({"metric_a", "metric_b"})
        data: dict[str, object] = {"name": "vol1", "metric_a": 100, "metric_b": 200, "size": 500}
        result = _strip_realtime_fields(data, rt)

        assert result == {"name": "vol1", "size": 500}

    def test_preserves_non_realtime_keys(self) -> None:
        """Non-realtime keys are preserved unchanged."""
        rt = frozenset({"metric_a"})
        data: dict[str, object] = {"name": "vol1", "size": 500}
        result = _strip_realtime_fields(data, rt)

        assert result == {"name": "vol1", "size": 500}

    def test_handles_nested_dicts(self) -> None:
        """Realtime keys are stripped recursively from nested dicts."""
        rt = frozenset({"metric_a"})
        data: dict[str, object] = {
            "name": "cluster1",
            "storage": {"name": "aggr1", "metric_a": 42, "capacity": 1024},
        }
        result = _strip_realtime_fields(data, rt)

        assert result == {
            "name": "cluster1",
            "storage": {"name": "aggr1", "capacity": 1024},
        }

    def test_handles_lists_of_dicts(self) -> None:
        """Realtime keys are stripped from dicts inside lists."""
        rt = frozenset({"metric_a"})
        data: dict[str, object] = {
            "volumes": [
                {"name": "vol1", "metric_a": 10},
                {"name": "vol2", "metric_a": 20},
            ],
        }
        result = _strip_realtime_fields(data, rt)

        assert result == {
            "volumes": [
                {"name": "vol1"},
                {"name": "vol2"},
            ],
        }

    def test_handles_lists_of_scalars(self) -> None:
        """Scalar lists are preserved unchanged."""
        rt = frozenset({"metric_a"})
        data: dict[str, object] = {"tags": ["a", "b", "c"]}
        result = _strip_realtime_fields(data, rt)

        assert result == {"tags": ["a", "b", "c"]}

    def test_empty_rt_attrs_returns_same_structure(self) -> None:
        """With no realtime attrs, the dict is returned unchanged."""
        rt: frozenset[str] = frozenset()
        data: dict[str, object] = {"name": "vol1", "size": 500}
        result = _strip_realtime_fields(data, rt)

        assert result == {"name": "vol1", "size": 500}

    def test_empty_dict_returns_empty(self) -> None:
        """An empty dict returns an empty dict."""
        rt = frozenset({"metric_a"})
        result = _strip_realtime_fields({}, rt)

        assert result == {}


class TestAllRealtimeAttrs:
    """Tests for all_realtime_attrs function."""

    def test_returns_non_empty_frozenset(self) -> None:
        """all_realtime_attrs returns a non-empty frozenset of realtime field names."""
        all_realtime_attrs.cache_clear()
        result = all_realtime_attrs()

        assert isinstance(result, frozenset)
        assert len(result) > 0

    def test_contains_known_realtime_field(self) -> None:
        """all_realtime_attrs includes known realtime cache_attr names."""
        all_realtime_attrs.cache_clear()
        result = all_realtime_attrs()

        # metric.duration is a realtime field on FC ports (and likely others)
        assert "metric.duration" in result
