"""OntapMetroclusterSvm type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.svms.model import (
    OntapMetroclusterSvm,
    OntapMetroclusterSvmArgument,
)


def _transform_failed_reason_arguments(
    record: dict[str, Any],
) -> list[OntapMetroclusterSvmArgument]:
    """Transform failed_reason.arguments into OntapMetroclusterSvmArgument list."""
    return [
        OntapMetroclusterSvmArgument(**item) for item in record.get("failed_reason.arguments", [])
    ]


ONTAPMETROCLUSTERSVM_MAPPING = TypeMapping(
    name="OntapMetroclusterSvm",
    model_class=OntapMetroclusterSvm,
    api_endpoint="/cluster/metrocluster/svms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cluster_name",
            api_path="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster_uuid",
            api_path="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="configuration_state",
            api_path="configuration_state",
        ),
        FieldMapping(
            cache_attr="failed_reason_arguments",
            api_path="failed_reason.arguments",
            transform=_transform_failed_reason_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="failed_reason_code",
            api_path="failed_reason.code",
        ),
        FieldMapping(
            cache_attr="failed_reason_message",
            api_path="failed_reason.message",
        ),
        FieldMapping(
            cache_attr="partner_svm_name",
            api_path="partner_svm.name",
        ),
        FieldMapping(
            cache_attr="partner_svm_uuid",
            api_path="partner_svm.uuid",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetroclusterSvm", ONTAPMETROCLUSTERSVM_MAPPING)
