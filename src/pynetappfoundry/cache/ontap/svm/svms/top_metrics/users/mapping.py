"""OntapTopMetricsSvmUser type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.svms.top_metrics.users.model import (
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
            cache_attr="iops.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="throughput.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="user_id",
        ),
        FieldMapping(
            cache_attr="user_name",
        ),
        FieldMapping(
            cache_attr="volumes",
            transform=_transform_volumes,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapTopMetricsSvmUser", ONTAPTOPMETRICSSVMUSER_MAPPING)
