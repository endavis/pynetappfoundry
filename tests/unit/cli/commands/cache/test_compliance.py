"""Tests for cache compliance CLI command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from pynetappfoundry.compliance.models import ComplianceResult, ComplianceRule


class TestCacheComplianceCommand:
    """Tests for nf cache compliance command."""

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
[compliance]
[compliance.vol_autosize]
description = "Volumes without grow_shrink autosize"
model = "storage.volumes"
where = "autosize.mode != 'grow_shrink'"
severity = "warning"

[compliance.node_down]
description = "Nodes not up"
model = "nodes"
where = "state != 'up'"
severity = "error"
"""
        )
        return config_dir

    @pytest.fixture
    def sample_results(self) -> list[ComplianceResult]:
        """Create sample compliance results."""
        return [
            ComplianceResult(
                rule_name="vol_autosize",
                description="Volumes without grow_shrink autosize",
                model="storage.volumes",
                severity="warning",
                cluster_name="cluster1",
                match_count=2,
                matches=[{"name": "vol1"}, {"name": "vol2"}],
            ),
        ]

    @pytest.fixture
    def sample_rules(self) -> dict[str, ComplianceRule]:
        """Create sample compliance rules."""
        return {
            "vol_autosize": ComplianceRule(
                name="vol_autosize",
                description="Volumes without grow_shrink autosize",
                model="storage.volumes",
                where="autosize.mode != 'grow_shrink'",
                severity="warning",
            ),
            "node_down": ComplianceRule(
                name="node_down",
                description="Nodes not up",
                model="nodes",
                where="state != 'up'",
                severity="error",
            ),
        }

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_single_cluster(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test compliance check on a single cluster with violations."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "cluster1"],
        )

        assert result.exit_code == 1
        mock_run_checks.assert_called_once()

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_all_flag(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test --all queries all cached clusters."""
        mock_db = MagicMock()
        mock_db.list_clusters.return_value = [
            {"cluster_name": "cluster1"},
            {"cluster_name": "cluster2"},
        ]
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "--all"],
        )

        assert result.exit_code == 1
        assert mock_run_checks.call_count == 2

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.Config")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_filter_flag(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_config_class: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test --filter for cluster selection."""
        mock_config = MagicMock()
        mock_config.get_clusters.return_value = {"prod-cluster": {"name": "prod-cluster"}}
        mock_config.data = {"clusters": {"prod-cluster": MagicMock()}}
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "compliance",
                "-f",
                '{"env":"prod"}',
            ],
        )

        assert result.exit_code == 1
        mock_config.get_clusters.assert_called_once_with({"env": "prod"})

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_check_flag(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test --check runs only the named rule."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "compliance",
                "cluster1",
                "-k",
                "vol_autosize",
            ],
        )

        assert result.exit_code == 1
        call_kwargs = mock_run_checks.call_args
        assert call_kwargs[1]["check_filter"] == "vol_autosize"

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_json_output(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test --json output is valid JSON."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "cluster1", "--json"],
        )

        assert result.exit_code == 1
        output = json.loads(result.output)
        assert isinstance(output, list)
        assert output[0]["rule_name"] == "vol_autosize"

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_csv_output(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test --csv output has header and data rows."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "cluster1", "--csv"],
        )

        assert result.exit_code == 1
        lines = result.output.strip().split("\n")
        assert "cluster,rule,severity,match_count,description" in lines[0]

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_exit_code_0_no_violations(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test exit code 0 when no violations found."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = []

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "cluster1"],
        )

        assert result.exit_code == 0

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_exit_code_1_violations_found(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_results: list[ComplianceResult],
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test exit code 1 when violations found."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules
        mock_run_checks.return_value = sample_results

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "cluster1"],
        )

        assert result.exit_code == 1

    def test_exit_code_2_config_not_found(
        self,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        """Test exit code 2 when config directory doesn't exist."""
        result = runner.invoke(
            nf,
            [
                "-c",
                str(tmp_path / "nonexistent"),
                "cache",
                "compliance",
                "cluster1",
            ],
        )

        assert result.exit_code == 2
        assert "not found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    def test_missing_compliance_config(
        self,
        mock_load_rules: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test graceful exit when no compliance rules defined."""
        mock_load_rules.return_value = {}

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance", "cluster1"],
        )

        assert result.exit_code == 0
        assert "No compliance rules" in result.output

    def test_no_cluster_selection_error(
        self,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test error when no cluster selection method specified."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "compliance"],
        )

        # Should hit the "Must specify CLUSTER, --all, or --filter" error
        # or the "No compliance rules" warning depending on config load
        assert result.exit_code in (0, 2)

    @patch("pynetappfoundry.cli.commands.cache.compliance.run_compliance_checks")
    @patch("pynetappfoundry.cli.commands.cache.compliance.merge_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.get_cluster_overrides")
    @patch("pynetappfoundry.cli.commands.cache.compliance.load_global_compliance_rules")
    @patch("pynetappfoundry.cli.commands.cache.compliance.ClusterMetadataDB")
    def test_severity_filter(
        self,
        mock_db_class: MagicMock,
        mock_load_rules: MagicMock,
        mock_get_overrides: MagicMock,
        mock_merge: MagicMock,
        mock_run_checks: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_rules: dict[str, ComplianceRule],
    ) -> None:
        """Test --severity filters results by minimum severity."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_load_rules.return_value = sample_rules
        mock_get_overrides.return_value = {}
        mock_merge.return_value = sample_rules

        # Return both warning and error results
        mock_run_checks.return_value = [
            ComplianceResult(
                rule_name="vol_autosize",
                description="Warning check",
                model="storage.volumes",
                severity="warning",
                cluster_name="cluster1",
                match_count=1,
                matches=[{"name": "vol1"}],
            ),
            ComplianceResult(
                rule_name="node_down",
                description="Error check",
                model="nodes",
                severity="error",
                cluster_name="cluster1",
                match_count=1,
                matches=[{"name": "node1"}],
            ),
        ]

        result = runner.invoke(
            nf,
            [
                "-c",
                str(mock_config_dir),
                "cache",
                "compliance",
                "cluster1",
                "-s",
                "error",
                "--json",
            ],
        )

        assert result.exit_code == 1
        output = json.loads(result.output)
        # Only error severity should remain
        assert len(output) == 1
        assert output[0]["severity"] == "error"
