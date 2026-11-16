"""AiqumSloLunGet type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.luns.model import AiqumSloLunGet

AIQUMSLOLUNGET_MAPPING = TypeMapping(
    name="AiqumSloLunGet",
    model_class=AiqumSloLunGet,
    api_endpoint="/storage-provider/luns",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="assigned_performance_service_level.expected_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="assigned_performance_service_level.key",
        ),
        FieldMapping(
            cache_attr="assigned_performance_service_level.name",
        ),
        FieldMapping(
            cache_attr="assigned_performance_service_level.peak_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="assigned_storage_efficiency_policy.key",
        ),
        FieldMapping(
            cache_attr="assigned_storage_efficiency_policy.name",
        ),
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.expected_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.key",
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.name",
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.peak_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volume.key",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumSloLunGet", AIQUMSLOLUNGET_MAPPING)
