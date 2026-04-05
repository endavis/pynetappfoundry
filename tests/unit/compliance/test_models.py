"""Tests for compliance data models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from pynetappfoundry.compliance.models import (
    ClusterComplianceOverride,
    ComplianceResult,
    ComplianceRule,
)


class TestComplianceRule:
    """Tests for ComplianceRule model."""

    def test_valid_rule(self) -> None:
        """Test creating a valid compliance rule."""
        rule = ComplianceRule(
            name="vol_autosize",
            description="Volumes without grow_shrink autosize",
            model="storage.volumes",
            where="autosize.mode != 'grow_shrink'",
            severity="warning",
            enabled=True,
        )
        assert rule.name == "vol_autosize"
        assert rule.model == "storage.volumes"
        assert rule.where == "autosize.mode != 'grow_shrink'"
        assert rule.severity == "warning"
        assert rule.enabled is True

    def test_defaults(self) -> None:
        """Test default values for optional fields."""
        rule = ComplianceRule(
            name="test",
            model="nodes",
            where="state != 'up'",
        )
        assert rule.description == ""
        assert rule.severity == "warning"
        assert rule.enabled is True

    def test_missing_required_model(self) -> None:
        """Test that missing 'model' raises ValidationError."""
        with pytest.raises(ValidationError):
            ComplianceRule(name="test", where="state != 'up'")  # type: ignore[call-arg]

    def test_missing_required_where(self) -> None:
        """Test that missing 'where' raises ValidationError."""
        with pytest.raises(ValidationError):
            ComplianceRule(name="test", model="nodes")  # type: ignore[call-arg]

    def test_missing_required_name(self) -> None:
        """Test that missing 'name' raises ValidationError."""
        with pytest.raises(ValidationError):
            ComplianceRule(model="nodes", where="state != 'up'")  # type: ignore[call-arg]


class TestClusterComplianceOverride:
    """Tests for ClusterComplianceOverride model."""

    def test_all_none_defaults(self) -> None:
        """Test that all fields default to None."""
        override = ClusterComplianceOverride()
        assert override.enabled is None
        assert override.description is None
        assert override.model is None
        assert override.where is None
        assert override.severity is None

    def test_partial_override(self) -> None:
        """Test override with only some fields set."""
        override = ClusterComplianceOverride(severity="error", enabled=False)
        assert override.severity == "error"
        assert override.enabled is False
        assert override.model is None
        assert override.where is None

    def test_full_override(self) -> None:
        """Test override with all fields set."""
        override = ClusterComplianceOverride(
            enabled=True,
            description="Custom description",
            model="storage.volumes",
            where="state = 'offline'",
            severity="error",
        )
        assert override.enabled is True
        assert override.description == "Custom description"
        assert override.model == "storage.volumes"
        assert override.where == "state = 'offline'"
        assert override.severity == "error"


class TestComplianceResult:
    """Tests for ComplianceResult model."""

    def test_construction(self) -> None:
        """Test creating a ComplianceResult."""
        result = ComplianceResult(
            rule_name="vol_autosize",
            description="Volume autosize check",
            model="storage.volumes",
            severity="warning",
            cluster_name="cluster1",
            match_count=2,
            matches=[{"name": "vol1"}, {"name": "vol2"}],
        )
        assert result.rule_name == "vol_autosize"
        assert result.cluster_name == "cluster1"
        assert result.match_count == 2
        assert len(result.matches) == 2

    def test_empty_matches(self) -> None:
        """Test result with zero matches."""
        result = ComplianceResult(
            rule_name="test",
            description="",
            model="nodes",
            severity="info",
            cluster_name="cluster1",
            match_count=0,
            matches=[],
        )
        assert result.match_count == 0
        assert result.matches == []
