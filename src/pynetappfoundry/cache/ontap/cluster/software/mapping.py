"""OntapSoftwareReference type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.software.model import (
    OntapSoftwareReference,
    OntapSoftwareReferenceMetroclusterCluster,
    OntapSoftwareReferenceNode,
    OntapSoftwareReferencePostUpdateCheck,
    OntapSoftwareReferenceStatusDetail,
    OntapSoftwareReferenceUpdateDetail,
    OntapSoftwareReferenceValidationResult,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_metrocluster_clusters(
    record: dict[str, Any],
) -> list[OntapSoftwareReferenceMetroclusterCluster]:
    """Transform metrocluster.clusters into OntapSoftwareReferenceMetroclusterCluster list."""
    try:
        items = get_nested_value(record, "metrocluster.clusters")
    except Exception:
        items = []
    return [OntapSoftwareReferenceMetroclusterCluster(**item) for item in items]


def _transform_nodes(record: dict[str, Any]) -> list[OntapSoftwareReferenceNode]:
    """Transform nodes into OntapSoftwareReferenceNode list."""
    return [OntapSoftwareReferenceNode(**item) for item in record.get("nodes", [])]


def _transform_post_update_checks(
    record: dict[str, Any],
) -> list[OntapSoftwareReferencePostUpdateCheck]:
    """Transform post_update_checks into OntapSoftwareReferencePostUpdateCheck list."""
    return [
        OntapSoftwareReferencePostUpdateCheck(**item)
        for item in record.get("post_update_checks", [])
    ]


def _transform_status_details(record: dict[str, Any]) -> list[OntapSoftwareReferenceStatusDetail]:
    """Transform status_details into OntapSoftwareReferenceStatusDetail list."""
    return [OntapSoftwareReferenceStatusDetail(**item) for item in record.get("status_details", [])]


def _transform_update_details(record: dict[str, Any]) -> list[OntapSoftwareReferenceUpdateDetail]:
    """Transform update_details into OntapSoftwareReferenceUpdateDetail list."""
    return [OntapSoftwareReferenceUpdateDetail(**item) for item in record.get("update_details", [])]


def _transform_validation_results(
    record: dict[str, Any],
) -> list[OntapSoftwareReferenceValidationResult]:
    """Transform validation_results into OntapSoftwareReferenceValidationResult list."""
    return [
        OntapSoftwareReferenceValidationResult(**item)
        for item in record.get("validation_results", [])
    ]


ONTAPSOFTWAREREFERENCE_MAPPING = TypeMapping(
    name="OntapSoftwareReference",
    model_class=OntapSoftwareReference,
    api_endpoint="/cluster/software?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="action",
        ),
        FieldMapping(
            cache_attr="elapsed_duration",
            default=0,
        ),
        FieldMapping(
            cache_attr="estimated_duration",
            default=0,
        ),
        FieldMapping(
            cache_attr="metrocluster.clusters",
            transform=_transform_metrocluster_clusters,
            default=[],
        ),
        FieldMapping(
            cache_attr="metrocluster.progress_details.message",
        ),
        FieldMapping(
            cache_attr="metrocluster.progress_summary.message",
        ),
        FieldMapping(
            cache_attr="nodes",
            transform=_transform_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="pending_version",
        ),
        FieldMapping(
            cache_attr="post_update_checks",
            transform=_transform_post_update_checks,
            default=[],
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="status_details",
            transform=_transform_status_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="update_details",
            transform=_transform_update_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="validation_results",
            transform=_transform_validation_results,
            default=[],
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping("OntapSoftwareReference", ONTAPSOFTWAREREFERENCE_MAPPING)
