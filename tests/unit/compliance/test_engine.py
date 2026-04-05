"""Tests for compliance check engine."""

from __future__ import annotations

from unittest.mock import MagicMock

from pynetappfoundry.compliance.engine import run_compliance_checks
from pynetappfoundry.compliance.models import ComplianceRule


class TestRunComplianceChecks:
    """Tests for run_compliance_checks."""

    def _make_mock_db(self, query_return: list | None = None) -> MagicMock:
        """Create a mock ClusterMetadataDB."""
        db = MagicMock()
        if query_return is not None:
            db.query_with_filters.return_value = query_return
        return db

    def _make_mock_match(self, data: dict) -> MagicMock:
        """Create a mock model instance with model_dump."""
        match = MagicMock()
        match.model_dump.return_value = data
        return match

    def test_returns_violations_when_matches(self) -> None:
        """Test that violations are returned when query finds matches."""
        match1 = self._make_mock_match({"name": "vol1", "state": "offline"})
        match2 = self._make_mock_match({"name": "vol2", "state": "offline"})
        db = self._make_mock_db([match1, match2])

        rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                description="Offline volumes",
                model="storage.volumes",
                where="state = 'offline'",
                severity="warning",
            ),
        }

        results = run_compliance_checks(db, "cluster1", rules)

        assert len(results) == 1
        assert results[0].rule_name == "vol_check"
        assert results[0].cluster_name == "cluster1"
        assert results[0].match_count == 2
        assert results[0].severity == "warning"
        db.query_with_filters.assert_called_once_with(
            "cluster1", "storage.volumes", ["state = 'offline'"]
        )

    def test_returns_empty_when_no_violations(self) -> None:
        """Test that empty list is returned when no matches found."""
        db = self._make_mock_db([])

        rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
            ),
        }

        results = run_compliance_checks(db, "cluster1", rules)

        assert results == []

    def test_disabled_rules_skipped(self) -> None:
        """Test that disabled rules are not executed."""
        db = self._make_mock_db()

        rules = {
            "disabled_check": ComplianceRule(
                name="disabled_check",
                model="nodes",
                where="state != 'up'",
                enabled=False,
            ),
        }

        results = run_compliance_checks(db, "cluster1", rules)

        assert results == []
        db.query_with_filters.assert_not_called()

    def test_check_filter_selects_named_rule(self) -> None:
        """Test that check_filter runs only the named rule."""
        match = self._make_mock_match({"name": "node1", "state": "down"})
        db = self._make_mock_db([match])

        rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
            ),
            "node_check": ComplianceRule(
                name="node_check",
                model="nodes",
                where="state != 'up'",
            ),
        }

        results = run_compliance_checks(db, "cluster1", rules, check_filter="node_check")

        assert len(results) == 1
        assert results[0].rule_name == "node_check"
        db.query_with_filters.assert_called_once_with("cluster1", "nodes", ["state != 'up'"])

    def test_value_error_handled_gracefully(self) -> None:
        """Test that ValueError from query is caught and rule is skipped."""
        db = MagicMock()
        db.query_with_filters.side_effect = ValueError("Unknown model name: 'bad.model'")

        rules = {
            "bad_check": ComplianceRule(
                name="bad_check",
                model="bad.model",
                where="x = 1",
            ),
        }

        results = run_compliance_checks(db, "cluster1", rules)

        assert results == []

    def test_multiple_rules(self) -> None:
        """Test running multiple rules, some with matches, some without."""
        match = self._make_mock_match({"name": "vol1"})
        db = MagicMock()
        db.query_with_filters.side_effect = [
            [match],  # vol_check finds violations
            [],  # node_check finds nothing
        ]

        rules = {
            "vol_check": ComplianceRule(
                name="vol_check",
                model="storage.volumes",
                where="state = 'offline'",
            ),
            "node_check": ComplianceRule(
                name="node_check",
                model="nodes",
                where="state != 'up'",
            ),
        }

        results = run_compliance_checks(db, "cluster1", rules)

        assert len(results) == 1
        assert results[0].rule_name == "vol_check"
