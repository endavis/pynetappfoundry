"""Tests for cache check CLI command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse


class TestCacheCheckCommand:
    """Tests for nf cache check command."""

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
    def sample_nodes(self) -> list[OntapNodeResponse]:
        """Create sample node models for testing."""
        return [
            OntapNodeResponse(
                name="node-01",
                uuid="00000000-0000-0000-0000-000000000001",
                serial_number="SN001",
                model_="FAS8200",
                state="up",
            ),
            OntapNodeResponse(
                name="node-02",
                uuid="00000000-0000-0000-0000-000000000002",
                serial_number="SN002",
                model_="FAS8200",
                state="up",
            ),
            OntapNodeResponse(
                name="node-03",
                uuid="00000000-0000-0000-0000-000000000003",
                serial_number="SN003",
                model_="AFF-A400",
                state="up",
            ),
        ]

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_single_cluster_with_where(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test single cluster query with --where filter returns matching results."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = sample_nodes[:2]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-w",
                "model_ = 'FAS8200'",
            ],
        )

        assert result.exit_code == 1  # matches found
        mock_db.query_with_filters.assert_called_once_with(
            "test-cluster", "nodes", ["model_ = 'FAS8200'"]
        )

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_all_queries_multiple_clusters(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test --all queries all cached clusters."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [
            {"cluster_name": "cluster1"},
            {"cluster_name": "cluster2"},
        ]
        mock_db.query_with_filters.side_effect = [
            sample_nodes[:1],
            sample_nodes[1:2],
        ]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "--all",
                "nodes",
                "-w",
                "state = 'up'",
            ],
        )

        assert result.exit_code == 1
        assert mock_db.query_with_filters.call_count == 2

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_fields_projection(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test --fields projects only requested fields."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = sample_nodes[:1]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-F",
                "name,serial_number",
            ],
        )

        assert result.exit_code == 1
        assert "node-01" in result.output
        assert "SN001" in result.output

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_json_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test --json output is valid JSON."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [sample_nodes[0]]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-F",
                "name,uuid",
                "--json",
            ],
        )

        assert result.exit_code == 1
        output = json.loads(result.output)
        assert "test-cluster" in output
        assert output["test-cluster"][0]["name"] == "node-01"
        assert output["test-cluster"][0]["uuid"] == "00000000-0000-0000-0000-000000000001"

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_csv_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test --csv output has header and data rows."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [sample_nodes[0]]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-F",
                "name,serial_number",
                "--csv",
            ],
        )

        assert result.exit_code == 1
        lines = result.output.strip().split("\n")
        assert lines[0] == "cluster,name,serial_number"
        assert "test-cluster,node-01,SN001" in lines[1]

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_count_output(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test --count outputs match count per cluster."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = sample_nodes[:2]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "--count",
            ],
        )

        assert result.exit_code == 1  # matches found
        assert "test-cluster: 2" in result.output

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_exit_code_0_no_matches(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test exit code 0 when no matches found."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-w",
                "name = 'nonexistent'",
            ],
        )

        assert result.exit_code == 0

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_exit_code_1_matches_found(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test exit code 1 when matches found."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [sample_nodes[0]]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
            ],
        )

        assert result.exit_code == 1

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_exit_code_2_invalid_model_name(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test exit code 2 on invalid model name."""
        mock_db = MagicMock()
        mock_db.query_with_filters.side_effect = ValueError("Unknown model name: 'invalid.model'")
        mock_db._registry = {"nodes": None, "storage.volumes": None}
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "invalid.model",
            ],
        )

        assert result.exit_code == 2
        assert "Unknown model name" in result.output
        assert "Available models:" in result.output

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_multiple_where_filters_and_joined(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test multiple --where expressions are AND-joined."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [sample_nodes[0]]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-w",
                "model_ = 'FAS8200'",
                "-w",
                "state = 'up'",
            ],
        )

        assert result.exit_code == 1
        mock_db.query_with_filters.assert_called_once_with(
            "test-cluster", "nodes", ["model_ = 'FAS8200'", "state = 'up'"]
        )

    def test_no_cluster_selection_error(
        self,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test error when no cluster selection method specified."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "check", "nodes"],
        )

        # Click will parse "nodes" as cluster, and there's no MODEL.
        # This should trigger a Click missing argument error or our validation.
        assert result.exit_code == 2

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_default_fields_include_name_uuid_where(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test default fields include name, uuid, and where field paths."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [sample_nodes[0]]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-w",
                "model_ = 'FAS8200'",
            ],
        )

        assert result.exit_code == 1
        # Default fields should include name, uuid, and model_ (from --where)
        assert "name" in result.output
        assert "uuid" in result.output
        assert "model_" in result.output

    @patch("pynetappfoundry.cli.commands.cache.check.Config")
    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_filter_cluster_selection(
        self,
        mock_db_class: MagicMock,
        mock_config_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_nodes: list[OntapNodeResponse],
    ) -> None:
        """Test --filter for cluster selection."""
        mock_config = MagicMock()
        mock_config.get_clusters.return_value = {"prod-cluster": {"name": "prod-cluster"}}
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [sample_nodes[0]]
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "-f",
                '{"env":"prod"}',
                "nodes",
                "-F",
                "name",
            ],
        )

        assert result.exit_code == 1
        mock_db.query_with_filters.assert_called_once_with("prod-cluster", "nodes", [])

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_count_zero_matches(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test --count with zero matches gives exit code 0."""
        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "check",
                "test-cluster",
                "nodes",
                "-w",
                "name = 'nonexistent'",
                "--count",
            ],
        )

        assert result.exit_code == 0
        assert "test-cluster: 0" in result.output

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
                "check",
                "cluster1",
                "nodes",
            ],
        )

        assert result.exit_code == 2
        assert "not found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.check.ClusterMetadataDB")
    def test_empty_cache_with_all(
        self,
        mock_db_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test --all with empty cache exits 0."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = []
        mock_db_class.return_value = mock_db

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "check", "--all", "nodes"],
        )

        assert result.exit_code == 0
        assert "No cached clusters" in result.output
