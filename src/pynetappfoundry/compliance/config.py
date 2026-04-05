"""Compliance rule loading and merging from TOML configuration.

Provides functions to load global compliance rules from the settings
TOML, extract per-cluster overrides from ClusterEntry data, and merge
them into an effective rule set for each cluster.
"""

from __future__ import annotations

import logging
from typing import Any

from pynetappfoundry.compliance.models import (
    ClusterComplianceOverride,
    ComplianceRule,
)
from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)


def load_global_compliance_rules(config: Config) -> dict[str, ComplianceRule]:
    """Load global compliance rules from the settings TOML.

    Reads the ``[compliance]`` section from ``config.get_setting()``.
    Each top-level key (except ``"settings"``) is treated as a rule name.

    Args:
        config: The application Config instance.

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
            logger.warning("Skipping non-dict compliance entry: %s", key)
            continue
        try:
            rules[key] = ComplianceRule(name=key, **data)
        except Exception:
            logger.warning("Invalid compliance rule %r, skipping", key)

    return rules


def get_cluster_overrides(
    cluster_entry: Any,
) -> dict[str, ClusterComplianceOverride]:
    """Extract per-cluster compliance overrides from a ClusterEntry.

    Looks for ``cluster_entry["checks"]["compliance"]`` and validates
    each key into a :class:`ClusterComplianceOverride`.

    Args:
        cluster_entry: A ClusterEntry (dict-like) for a single cluster.

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
            logger.warning("Skipping non-dict cluster compliance override: %s", key)
            continue
        try:
            overrides[key] = ClusterComplianceOverride(**data)
        except Exception:
            logger.warning("Invalid cluster compliance override %r, skipping", key)

    return overrides


def merge_rules(
    global_rules: dict[str, ComplianceRule],
    overrides: dict[str, ClusterComplianceOverride],
) -> dict[str, ComplianceRule]:
    """Merge global rules with per-cluster overrides.

    For each global rule, applies non-None override fields using
    ``model_copy(update=...)``. For override keys not present in the
    global rules, constructs a new ComplianceRule (requires ``model``
    and ``where`` to be set in the override).

    Args:
        global_rules: Dict of global ComplianceRule instances.
        overrides: Dict of per-cluster overrides.

    Returns:
        New dict of effective ComplianceRule instances.
    """
    merged: dict[str, ComplianceRule] = {}

    for name, rule in global_rules.items():
        if name in overrides:
            override = overrides[name]
            update_fields = {k: v for k, v in override.model_dump().items() if v is not None}
            merged[name] = rule.model_copy(update=update_fields)
        else:
            merged[name] = rule.model_copy()

    # Cluster-specific rules not in global
    for name, override in overrides.items():
        if name not in global_rules:
            override_data = {k: v for k, v in override.model_dump().items() if v is not None}
            try:
                merged[name] = ComplianceRule(name=name, **override_data)
            except Exception:
                logger.warning(
                    "Cluster-specific rule %r missing required fields (model, where), skipping",
                    name,
                )

    return merged
