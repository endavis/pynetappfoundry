"""Compliance check execution engine.

Runs compliance rules against cached cluster metadata and returns
violation results.
"""

from __future__ import annotations

import logging

from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.compliance.models import ComplianceResult, ComplianceRule

logger = logging.getLogger(__name__)


def run_compliance_checks(
    db: ClusterMetadataDB,
    cluster_name: str,
    rules: dict[str, ComplianceRule],
    check_filter: str | None = None,
) -> list[ComplianceResult]:
    """Execute compliance rules against a single cluster's cached data.

    For each enabled rule, queries the cache DB using the rule's model
    and filter expression. Any matching records represent violations.

    Args:
        db: An open ClusterMetadataDB instance.
        cluster_name: Name of the cluster to check.
        rules: Dict of effective ComplianceRule instances.
        check_filter: If provided, only run the rule with this name.

    Returns:
        List of ComplianceResult for each rule that found violations.
    """
    results: list[ComplianceResult] = []

    for name, rule in rules.items():
        if check_filter is not None and name != check_filter:
            continue

        if not rule.enabled:
            logger.debug("Skipping disabled rule: %s", name)
            continue

        try:
            matches = db.query_with_filters(cluster_name, rule.model, [rule.where])
        except ValueError as e:
            logger.warning("Rule %r query failed for cluster %s: %s", name, cluster_name, e)
            continue

        if not matches:
            continue

        match_dicts = [m.model_dump() for m in matches]
        results.append(
            ComplianceResult(
                rule_name=name,
                description=rule.description,
                model=rule.model,
                severity=rule.severity,
                cluster_name=cluster_name,
                match_count=len(match_dicts),
                matches=match_dicts,
            )
        )

    return results
