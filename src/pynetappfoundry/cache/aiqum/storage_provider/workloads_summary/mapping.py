"""AiqumWorkloadsSummary type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.workloads_summary.model import (
    AiqumWorkloadsSummary,
    AiqumWorkloadsSummaryPerformanceServiceLevelSummaryPerformanceServiceLevel,
)

AIQUMWORKLOADSSUMMARY_MAPPING = TypeMapping(
    name="AiqumWorkloadsSummary",
    model_class=AiqumWorkloadsSummary,
    api_endpoint="/storage-provider/workloads-summary",
    api_type="aiqum",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="conformance_summary.conformant_workload_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="conformance_summary.non_conformant_workload_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="conformance_summary.workload_with_unknown_status_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="iops.available",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="iops.total",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="iops.used",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="performance_service_level_summary.managed_workload_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="performance_service_level_summary.performance_service_levels",
            item_model=AiqumWorkloadsSummaryPerformanceServiceLevelSummaryPerformanceServiceLevel,
            default=[],
        ),
        FieldMapping(
            cache_attr="performance_service_level_summary.unmanaged_workload_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="performance_service_level_summary.workloads_with_system_suggested_psls",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.available",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="total_workload_count",
            default=0,
        ),
    ),
)

model_registry.register_mapping("AiqumWorkloadsSummary", AIQUMWORKLOADSSUMMARY_MAPPING)
