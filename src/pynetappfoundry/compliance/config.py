"""Compliance rule loading and merging from TOML configuration.

Provides functions to load global compliance rules from the settings
TOML, extract per-cluster overrides from ClusterEntry data, and merge
them into an effective rule set for each cluster.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import ValidationError

from pynetappfoundry.compliance.models import (
    ClusterComplianceOverride,
    ComplianceRule,
    ComplianceRuleError,
    RuleErrorStage,
)
from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)


def _format_validation_error(exc: ValidationError) -> str:
    """Summarise a pydantic ValidationError as ``field: reason`` pairs.

    Args:
        exc: The validation error.

    Returns:
        A single-line message naming each failing field and its reason.
    """
    parts = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "<rule>"
        parts.append(f"{loc}: {err['msg']}")
    return "; ".join(parts)


def _record(
    errors: list[ComplianceRuleError] | None,
    rule_name: str,
    cluster_name: str | None,
    stage: RuleErrorStage,
    message: str,
) -> None:
    """Log a rule failure and append it to the collector when one is given.

    Args:
        errors: Optional collector.
        rule_name: Rule (table key) that failed.
        cluster_name: Cluster the failure applies to, or None for global rules.
        stage: Stage at which the failure happened.
        message: Reason for the failure.
    """
    logger.warning("Compliance rule %r (%s) skipped: %s", rule_name, stage, message)
    if errors is not None:
        errors.append(
            ComplianceRuleError(
                rule_name=rule_name,
                cluster_name=cluster_name,
                stage=stage,
                message=message,
            )
        )


def load_global_compliance_rules(
    config: Config,
    errors: list[ComplianceRuleError] | None = None,
) -> dict[str, ComplianceRule]:
    """Load global compliance rules from the settings TOML.

    Reads the ``[compliance]`` section from ``config.get_setting()``.
    Each top-level key (except ``"settings"``) is treated as a rule name.
    A ``name`` key inside a rule table is rejected: the table key is the name.

    Args:
        config: The application Config instance.
        errors: If provided, each invalid rule is recorded here with its reason.

    Returns:
        Dict mapping rule name to ComplianceRule.
    """
    raw_value: dict[str, Any] | Any = config.get_setting("compliance", default={})
    raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
    rules: dict[str, ComplianceRule] = {}

    for key, data in raw.items():
        if key == "settings":
            continue
        if not isinstance(data, dict):
            _record(errors, key, None, "load", "rule must be a table, not a scalar value")
            continue
        if "name" in data:
            _record(
                errors,
                key,
                None,
                "load",
                "'name' is reserved: the table key is the rule name; remove the 'name' field",
            )
            continue
        try:
            rules[key] = ComplianceRule(name=key, **data)
        except ValidationError as e:
            _record(errors, key, None, "load", _format_validation_error(e))

    return rules


def get_cluster_overrides(
    cluster_entry: Any,
    errors: list[ComplianceRuleError] | None = None,
    cluster_name: str | None = None,
) -> dict[str, ClusterComplianceOverride]:
    """Extract per-cluster compliance overrides from a ClusterEntry.

    Looks for ``cluster_entry["checks"]["compliance"]`` and validates
    each key into a :class:`ClusterComplianceOverride`.

    Args:
        cluster_entry: A ClusterEntry (dict-like) for a single cluster.
        errors: If provided, each invalid override is recorded here.
        cluster_name: Cluster name recorded on any error.

    Returns:
        Dict mapping rule name to ClusterComplianceOverride.
    """
    checks = cluster_entry.get("checks", {})
    if not isinstance(checks, dict):
        return {}
    compliance_section = checks.get("compliance", {})
    if not isinstance(compliance_section, dict):
        return {}

    overrides: dict[str, ClusterComplianceOverride] = {}
    for key, data in compliance_section.items():
        if not isinstance(data, dict):
            _record(errors, key, cluster_name, "override", "override must be a table, not a scalar")
            continue
        try:
            overrides[key] = ClusterComplianceOverride(**data)
        except ValidationError as e:
            _record(errors, key, cluster_name, "override", _format_validation_error(e))

    return overrides


def merge_rules(
    global_rules: dict[str, ComplianceRule],
    overrides: dict[str, ClusterComplianceOverride],
    errors: list[ComplianceRuleError] | None = None,
    cluster_name: str | None = None,
) -> dict[str, ComplianceRule]:
    """Merge global rules with per-cluster overrides.

    For each global rule, applies non-None override fields and re-validates
    the result. A rule whose merged form is invalid is omitted for this
    cluster and recorded. For override keys not present in the global rules,
    constructs a new ComplianceRule (requires ``model`` and ``where`` to be
    set in the override).

    Args:
        global_rules: Dict of global ComplianceRule instances.
        overrides: Dict of per-cluster overrides.
        errors: If provided, each rule that cannot be built is recorded here.
        cluster_name: Cluster name recorded on any error.

    Returns:
        New dict of effective ComplianceRule instances.
    """
    merged: dict[str, ComplianceRule] = {}

    for name, rule in global_rules.items():
        if name in overrides:
            override = overrides[name]
            update_fields = {k: v for k, v in override.model_dump().items() if v is not None}
            try:
                merged[name] = ComplianceRule.model_validate({**rule.model_dump(), **update_fields})
            except ValidationError as e:
                _record(errors, name, cluster_name, "merge", _format_validation_error(e))
        else:
            merged[name] = rule.model_copy()

    # Cluster-specific rules not in global
    for name, override in overrides.items():
        if name not in global_rules:
            override_data = {k: v for k, v in override.model_dump().items() if v is not None}
            try:
                merged[name] = ComplianceRule(name=name, **override_data)
            except ValidationError as e:
                _record(errors, name, cluster_name, "merge", _format_validation_error(e))

    return merged
