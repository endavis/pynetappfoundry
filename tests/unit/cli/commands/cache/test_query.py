"""Tests for cache query CLI command."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache.models import (
    CachedClusterMetadata,
    CloudMetadata,
    ClusterInfo,
    NodeInfo,
)
from pynetappfoundry.cli.main import nf


class TestCacheQueryCommand:
    """Tests for nf cache query command."""

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
            cloud=[
                CloudMetadata(
                    provider="AWS",
                    region="us-east-1",
                    instance_type="m5.xlarge",
                )
            ],
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                cluster_uuid="abc-123",
                ontap_version="9.14.1",
            ),
            nodes=[
                NodeInfo(name="node-01", serial_number="SN001"),
                NodeInfo(name="node-02", serial_number="SN002"),
            ],
        )

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_single_cluster_single_field(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test querying a single field from a single cluster."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "test-cluster", "cloud[0].provider"],
        )

        assert result.exit_code == 0
        assert "test-cluster:" in result.output
        assert "cloud[0].provider: AWS" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_single_cluster_multiple_fields(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test querying multiple fields from a single cluster."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cloud[0].provider",
                "cluster.ontap_version",
            ],
        )

        assert result.exit_code == 0
        assert "cloud[0].provider: AWS" in result.output
        assert "cluster.ontap_version: 9.14.1" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_query_all_clusters(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test querying all cached clusters."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [
            {"cluster_name": "cluster1"},
            {"cluster_name": "cluster2"},
        ]

        metadata1 = CachedClusterMetadata(
            cluster_name="cluster1",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="AWS", instance_type="m5.xlarge")],
        )
        metadata2 = CachedClusterMetadata(
            cluster_name="cluster2",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="Azure", instance_type="Standard_D4s_v3")],
        )
        mock_db.get.side_effect = lambda name: metadata1 if name == "cluster1" else metadata2
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "--all", "cloud[0].instance_type"],
        )

        assert result.exit_code == 0
        assert "cluster1:" in result.output
        assert "cloud[0].instance_type: m5.xlarge" in result.output
        assert "cluster2:" in result.output
        assert "cloud[0].instance_type: Standard_D4s_v3" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.Config")
    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_query_with_filter(
        self,
        mock_db_class: MagicMock,
        mock_config_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test querying clusters with JSON filter."""
        mock_config = MagicMock()
        mock_config.get_clusters.return_value = {"prod-cluster": {"name": "prod-cluster"}}
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        metadata = CachedClusterMetadata(
            cluster_name="prod-cluster",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="AWS", region="us-east-1")],
        )
        mock_db.get.return_value = metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "-f",
                '{"env":"prod"}',
                "cloud[0].provider",
                "cloud[0].region",
            ],
        )

        assert result.exit_code == 0
        assert "prod-cluster:" in result.output
        assert "cloud[0].provider: AWS" in result.output
        assert "cloud[0].region: us-east-1" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_json_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test JSON output format."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cloud[0].instance_type",
                "--json",
            ],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output == {"test-cluster": {"cloud[0].instance_type": "m5.xlarge"}}

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_raw_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test raw output format."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cluster.ontap_version",
                "--raw",
            ],
        )

        assert result.exit_code == 0
        assert result.output.strip() == "9.14.1"

    def test_raw_with_multiple_clusters_error(
        self,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that --raw errors when used with --all."""
        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "--all",
                "cloud[0].provider",
                "--raw",
            ],
        )

        assert result.exit_code != 0
        assert "--raw is only valid when querying a single cluster" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_array_index_access(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test querying array elements by index."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "test-cluster", "nodes[0].name"],
        )

        assert result.exit_code == 0
        assert "nodes[0].name: node-01" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_invalid_field_path_error(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test error when field path doesn't exist."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "test-cluster", "invalid.path"],
        )

        assert result.exit_code != 0
        assert "not found" in result.output.lower()

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_missing_cluster_error(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test error when cluster doesn't exist in cache."""
        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "nonexistent", "cloud[0].provider"],
        )

        assert result.exit_code != 0
        assert "No cached data" in result.output or "No results found" in result.output

    def test_no_cluster_or_all_or_filter_error(
        self,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test error when no cluster selection method specified."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "cloud[0].provider"],
        )

        # Click will parse "cloud[0].provider" as the CLUSTER argument but no fields
        # So we expect an error about missing fields
        assert result.exit_code != 0

    def test_no_fields_error(
        self,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test error when no fields specified."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "--all"],
        )

        assert result.exit_code != 0
        assert "FIELD" in result.output or "field" in result.output.lower()

    def test_config_not_found_error(
        self,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        """Test error when config directory doesn't exist."""
        result = runner.invoke(
            nf,
            [
                "-c",
                str(tmp_path / "nonexistent"),
                "cache",
                "query",
                "cluster1",
                "cloud[0].provider",
            ],
        )

        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_positional_args_with_all_treated_as_fields(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that positional args with --all are treated as fields, not cluster."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [{"cluster_name": "cluster1"}]
        metadata = CachedClusterMetadata(
            cluster_name="cluster1",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="AWS", region="us-east-1")],
        )
        mock_db.get.return_value = metadata
        mock_db_class.return_value = mock_db

        # With --all, both positional args should be treated as fields
        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "--all",
                "cloud[0].provider",
                "cloud[0].region",
            ],
        )

        assert result.exit_code == 0
        assert "cloud[0].provider: AWS" in result.output
        assert "cloud[0].region: us-east-1" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_empty_cache_with_all(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test --all with empty cache."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "--all", "cloud[0].provider"],
        )

        assert result.exit_code == 0
        assert "No cached clusters" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.Config")
    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_filter_no_matches(
        self,
        mock_db_class: MagicMock,
        mock_config_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test filter with no matching clusters."""
        mock_config = MagicMock()
        mock_config.get_clusters.return_value = {}
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "-f",
                '{"env":"nonexistent"}',
                "cloud[0].provider",
            ],
        )

        assert result.exit_code == 0
        assert "No clusters match the filter" in result.output

    def test_invalid_filter_json(
        self,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test error with invalid filter JSON."""
        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "-f",
                "not valid json",
                "cloud[0].provider",
            ],
        )

        assert result.exit_code != 0
        assert "Invalid filter JSON" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_multiple_fields_json_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test JSON output with multiple fields."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cloud[0].provider",
                "cloud[0].region",
                "cluster.ontap_version",
                "--json",
            ],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output == {
            "test-cluster": {
                "cloud[0].provider": "AWS",
                "cloud[0].region": "us-east-1",
                "cluster.ontap_version": "9.14.1",
            }
        }

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_raw_output_multiple_fields(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test raw output with multiple fields (one value per line)."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cloud[0].provider",
                "cluster.ontap_version",
                "--raw",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines == ["AWS", "9.14.1"]

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_query_boolean_value(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test querying a boolean value."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "test-cluster", "ha.is_ha", "--raw"],
        )

        assert result.exit_code == 0
        assert result.output.strip() == "false"

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_query_nested_array(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test querying nested array with multiple indices."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "nodes[1].serial_number",
            ],
        )

        assert result.exit_code == 0
        assert "SN002" in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_wildcard_array_access(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test querying all array elements with wildcard [*] syntax."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "query", "test-cluster", "nodes[*].name"],
        )

        assert result.exit_code == 0
        assert "test-cluster:" in result.output
        assert '["node-01", "node-02"]' in result.output

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_wildcard_json_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test wildcard query with JSON output."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "nodes[*].name",
                "--json",
            ],
        )

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output == {"test-cluster": {"nodes[*].name": ["node-01", "node-02"]}}

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_wildcard_raw_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test wildcard query with raw output (one value per line)."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "nodes[*].name",
                "--raw",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines == ["node-01", "node-02"]

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_wildcard_serial_numbers(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test wildcard query for serial numbers."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "nodes[*].serial_number",
                "--raw",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines == ["SN001", "SN002"]

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_csv_output_single_cluster(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test CSV output format with single cluster."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cloud[0].provider",
                "cloud[0].region",
                "--csv",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines[0] == "cluster,cloud[0].provider,cloud[0].region"
        assert lines[1] == "test-cluster,AWS,us-east-1"

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_csv_output_multiple_clusters(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test CSV output format with multiple clusters."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [
            {"cluster_name": "cluster1"},
            {"cluster_name": "cluster2"},
        ]

        metadata1 = CachedClusterMetadata(
            cluster_name="cluster1",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="AWS", region="us-east-1")],
        )
        metadata2 = CachedClusterMetadata(
            cluster_name="cluster2",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="Azure", region="eastus")],
        )
        mock_db.get.side_effect = lambda name: metadata1 if name == "cluster1" else metadata2
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "--all",
                "cloud[0].provider",
                "cloud[0].region",
                "--csv",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines[0] == "cluster,cloud[0].provider,cloud[0].region"
        assert "cluster1,AWS,us-east-1" in lines
        assert "cluster2,Azure,eastus" in lines

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_csv_output_with_wildcard(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test CSV output with wildcard expands to multiple rows."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "nodes[*].name",
                "nodes[*].serial_number",
                "--csv",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines[0] == "cluster,nodes[*].name,nodes[*].serial_number"
        assert lines[1] == "test-cluster,node-01,SN001"
        assert lines[2] == "test-cluster,node-02,SN002"

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_csv_output_with_boolean(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test CSV output formats boolean values correctly."""
        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "ha.is_ha",
                "--csv",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines[0] == "cluster,ha.is_ha"
        assert lines[1] == "test-cluster,false"

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_csv_output_with_empty_value(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test CSV output handles empty string values correctly."""
        mock_db = MagicMock()
        metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            cached_at=datetime(2024, 1, 15, tzinfo=UTC),
            cloud=[CloudMetadata(provider="AWS", region="")],
        )
        mock_db.get.return_value = metadata
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "query",
                "test-cluster",
                "cloud[0].provider",
                "cloud[0].region",
                "--csv",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert lines[0] == "cluster,cloud[0].provider,cloud[0].region"
        assert lines[1] == "test-cluster,AWS,"
