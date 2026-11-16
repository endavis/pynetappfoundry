"""AiqumStorageProviderPerformanceServiceLevel type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.performance_service_levels.model import (
    AiqumStorageProviderPerformanceServiceLevel,
)

AIQUMSTORAGEPROVIDERPERFORMANCESERVICELEVEL_MAPPING = TypeMapping(
    name="AiqumStorageProviderPerformanceServiceLevel",
    model_class=AiqumStorageProviderPerformanceServiceLevel,
    api_endpoint="/storage-provider/performance-service-levels",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="iops.absolute_min_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.expected_iops_per_tb",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.peak_iops_allocation_policy",
        ),
        FieldMapping(
            cache_attr="iops.peak_iops_per_tb",
            default=0,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="latency.expected",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="space.available",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="system_defined",
            default=False,
        ),
        FieldMapping(
            cache_attr="update_time",
        ),
        FieldMapping(
            cache_attr="workload_count",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "AiqumStorageProviderPerformanceServiceLevel",
    AIQUMSTORAGEPROVIDERPERFORMANCESERVICELEVEL_MAPPING,
)
