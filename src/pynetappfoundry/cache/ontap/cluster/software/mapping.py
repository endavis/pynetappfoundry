"""OntapSoftwareReference type mapping."""

from __future__ import annotations

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
            item_model=OntapSoftwareReferenceMetroclusterCluster,
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
            item_model=OntapSoftwareReferenceNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="pending_version",
        ),
        FieldMapping(
            cache_attr="post_update_checks",
            item_model=OntapSoftwareReferencePostUpdateCheck,
            default=[],
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="status_details",
            item_model=OntapSoftwareReferenceStatusDetail,
            default=[],
        ),
        FieldMapping(
            cache_attr="update_details",
            item_model=OntapSoftwareReferenceUpdateDetail,
            default=[],
        ),
        FieldMapping(
            cache_attr="validation_results",
            item_model=OntapSoftwareReferenceValidationResult,
            default=[],
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping("OntapSoftwareReference", ONTAPSOFTWAREREFERENCE_MAPPING)
