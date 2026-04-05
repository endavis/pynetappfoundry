"""Tests for compliance configuration loading and merging."""

from __future__ import annotations

from unittest.mock import MagicMock

from pynetappfoundry.compliance.config import (
    get_cluster_overrides,
    load_global_compliance_rules,
    merge_rules,
)
from pynetappfoundry.compliance.models import (
    ClusterComplianceOverride,
    ComplianceRule,
)


class TestLoadGlobalComplianceRules:
    """Tests for load_global_compliance_rules."""

    def test_loads_rules_from_config(self) -> None:
        """Test loading valid compliance rules from config."""
        mock_config = MagicMock()
        mock_config.get_setting.return_value = {
            "vol_autosize": {
                "description": "Autosize check",
                "model": "storage.volumes",
                "where": "autosize.mode != 'grow_shrink'",
                "severity": "warning",
            },
            "node_down": {
                "description": "Node down",
                "model": "nodes",
                "where": "state != 'up'",
                "severity": "error",
            },
        }

        rules = load_global_compliance_rules(mock_config)

        assert len(rules) == 2
        assert "vol_autosize" in rules
        assert "node_down" in rules
        assert rules["vol_autosize"].model == "storage.volumes"
        assert rules["node_down"].severity == "error"
        mock_config.get_setting.assert_called_once_with("compliance", default={})

    def test_empty_config(self) -> None:
        """Test loading when no compliance section exists."""
        mock_config = MagicMock()
        mock_config.get_setting.return_value = {}

        rules = load_global_compliance_rules(mock_config)

        assert rules == {}

    def test_skips_settings_key(self) -> None:
        """Test that the 'settings' key is skipped."""
        mock_config = MagicMock()
        mock_config.get_setting.return_value = {
            "settings": {"timeout": 30},
            "vol_check": {
                "model": "storage.volumes",
                "where": "state = 'offline'",
            },
        }

        rules = load_global_compliance_rules(mock_config)

        assert len(rules) == 1
        assert "settings" not in rules
        assert "vol_check" in rules

    def test_skips_invalid_rules(self) -> None:
        """Test that invalid rule dicts are skipped."""
        mock_config = MagicMock()
        mock_config.get_setting.return_value = {
            "valid": {
                "model": "nodes",
                "where": "state != 'up'",
            },
            "invalid": "not-a-dict",
        }

        rules = load_global_compliance_rules(mock_config)

        assert len(rules) == 1
        assert "valid" in rules


class TestGetClusterOverrides:
    """Tests for get_cluster_overrides."""

    def test_extracts_overrides(self) -> None:
        """Test extracting compliance overrides from a cluster entry."""
        cluster_entry = MagicMock()
        cluster_entry.get.return_value = {
            "compliance": {
                "vol_autosize": {"severity": "error"},
                "node_down": {"enabled": False},
            }
        }

        overrides = get_cluster_overrides(cluster_entry)

        assert len(overrides) == 2
        assert overrides["vol_autosize"].severity == "error"
        assert overrides["node_down"].enabled is False

    def test_missing_checks_key(self) -> None:
        """Test when cluster entry has no 'checks' key."""
        cluster_entry = MagicMock()
        cluster_entry.get.return_value = {}

        overrides = get_cluster_overrides(cluster_entry)

        assert overrides == {}

    def test_empty_compliance_section(self) -> None:
        """Test when compliance section is empty."""
        cluster_entry = MagicMock()
        cluster_entry.get.return_value = {"compliance": {}}

        overrides = get_cluster_overrides(cluster_entry)

        assert overrides == {}

    def test_non_dict_checks(self) -> None:
        """Test when 'checks' is not a dict."""
        cluster_entry = MagicMock()
        cluster_entry.get.return_value = "not-a-dict"

        overrides = get_cluster_overrides(cluster_entry)

        assert overrides == {}


class TestMergeRules:
    """Tests for merge_rules."""

    def test_override_severity(self) -> None:
        """Test overriding a rule's severity."""
        global_rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
                severity="warning",
            ),
        }
        overrides = {
            "vol_check": ClusterComplianceOverride(severity="error"),
        }

        merged = merge_rules(global_rules, overrides)

        assert merged["vol_check"].severity == "error"
        assert merged["vol_check"].model == "storage.volumes"

    def test_disable_check(self) -> None:
        """Test disabling a rule via override."""
        global_rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
                enabled=True,
            ),
        }
        overrides = {
            "vol_check": ClusterComplianceOverride(enabled=False),
        }

        merged = merge_rules(global_rules, overrides)

        assert merged["vol_check"].enabled is False

    def test_override_where(self) -> None:
        """Test overriding a rule's where expression."""
        global_rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
            ),
        }
        overrides = {
            "vol_check": ClusterComplianceOverride(where="state = 'error'"),
        }

        merged = merge_rules(global_rules, overrides)

        assert merged["vol_check"].where == "state = 'error'"

    def test_no_overrides_identity(self) -> None:
        """Test that no overrides returns equivalent rules."""
        global_rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
                severity="warning",
            ),
        }

        merged = merge_rules(global_rules, {})

        assert len(merged) == 1
        assert merged["vol_check"].model == "storage.volumes"
        assert merged["vol_check"].severity == "warning"

    def test_cluster_specific_check(self) -> None:
        """Test adding a cluster-specific rule not in global rules."""
        global_rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
            ),
        }
        overrides = {
            "custom_check": ClusterComplianceOverride(
                model="nodes",
                where="state != 'up'",
                severity="error",
            ),
        }

        merged = merge_rules(global_rules, overrides)

        assert len(merged) == 2
        assert "custom_check" in merged
        assert merged["custom_check"].model == "nodes"
        assert merged["custom_check"].severity == "error"

    def test_cluster_specific_check_missing_required_fields(self) -> None:
        """Test that cluster-specific rules without required fields are skipped."""
        global_rules = {}
        overrides = {
            "incomplete": ClusterComplianceOverride(severity="error"),
        }

        merged = merge_rules(global_rules, overrides)

        assert "incomplete" not in merged

    def test_does_not_mutate_global_rules(self) -> None:
        """Test that merge_rules does not mutate the input global_rules dict."""
        global_rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
                severity="warning",
            ),
        }
        overrides = {
            "vol_check": ClusterComplianceOverride(severity="error"),
        }

        merge_rules(global_rules, overrides)

        assert global_rules["vol_check"].severity == "warning"
