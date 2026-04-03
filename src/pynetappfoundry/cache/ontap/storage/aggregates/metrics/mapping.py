"""OntapPerformanceMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.aggregates.metrics.model import (
    OntapPerformanceMetricResponse,
)

ONTAPPERFORMANCEMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceMetricResponse",
    model_class=OntapPerformanceMetricResponse,
    api_endpoint="/storage/aggregates/{uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapAggregate",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="iops.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="throughput.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
        ),
    ),
)

model_registry.register_mapping(
    "OntapPerformanceMetricResponse", ONTAPPERFORMANCEMETRICRESPONSE_MAPPING
)
