"""Compliance check data models.

Defines the Pydantic models used to represent compliance rules,
per-cluster overrides, and check results.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ComplianceRule(BaseModel):
    """A single compliance rule definition.

    Attributes:
        name: Rule identifier (key from TOML config).
        description: Human-readable description of the rule.
        model: Cache model path (e.g. ``"storage.volumes"``).
        where: Filter expression for the query engine.
        severity: Severity level (``"info"``, ``"warning"``, ``"error"``).
        enabled: Whether the rule is active.
    """

    name: str
    description: str = ""
    model: str
    where: str
    severity: str = "warning"
    enabled: bool = True


class ClusterComplianceOverride(BaseModel):
    """Per-cluster override for a compliance rule.

    All fields are optional; only non-None values override the global rule.

    Attributes:
        enabled: Override enabled state.
        description: Override description.
        model: Override model path.
        where: Override filter expression.
        severity: Override severity level.
    """

    enabled: bool | None = None
    description: str | None = None
    model: str | None = None
    where: str | None = None
    severity: str | None = None


class ComplianceResult(BaseModel):
    """Result of a single compliance check against one cluster.

    Attributes:
        rule_name: Name of the rule that was violated.
        description: Rule description.
        model: Cache model path that was queried.
        severity: Severity of the violation.
        cluster_name: Name of the cluster checked.
        match_count: Number of matching (violating) records.
        matches: List of model dicts representing violations.
    """

    rule_name: str
    description: str
    model: str
    severity: str
    cluster_name: str
    match_count: int
    matches: list[dict[str, Any]]
