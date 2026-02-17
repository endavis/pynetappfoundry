"""OntapTopMetricsSvmUser type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.svm.svms.top_metrics.users.model import (
    OntapTopMetricsSvmUser,
    OntapTopMetricsSvmUserVolume,
)


def _transform_volumes(record: dict[str, Any]) -> list[OntapTopMetricsSvmUserVolume]:
    """Transform volumes into OntapTopMetricsSvmUserVolume list."""
    return [OntapTopMetricsSvmUserVolume(**item) for item in record.get("volumes", [])]


ONTAPTOPMETRICSSVMUSER_MAPPING = TypeMapping(
    name="OntapTopMetricsSvmUser",
    model_class=OntapTopMetricsSvmUser,
    api_endpoint="/svm/svms/{svm.uuid}/top-metrics/users?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="iops_error_lower_bound",
            api_path="iops.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_error_upper_bound",
            api_path="iops.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_read",
            api_path="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_write",
            api_path="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="throughput_error_lower_bound",
            api_path="throughput.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_error_upper_bound",
            api_path="throughput.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="user_id",
            api_path="user_id",
        ),
        FieldMapping(
            cache_attr="user_name",
            api_path="user_name",
        ),
        FieldMapping(
            cache_attr="volumes",
            transform=_transform_volumes,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapTopMetricsSvmUser", ONTAPTOPMETRICSSVMUSER_MAPPING)
