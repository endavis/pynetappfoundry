"""AiqumAggregateMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.aggregates.metrics.model import (
    AiqumAggregateMetricsSampleResponse,
)

AIQUMAGGREGATEMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumAggregateMetricsSampleResponse",
    model_class=AiqumAggregateMetricsSampleResponse,
    api_endpoint="/datacenter/storage/aggregates/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumAggregate",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="aggregate.key",
        ),
        FieldMapping(
            cache_attr="aggregate.name",
        ),
        FieldMapping(
            cache_attr="aggregate.uuid",
        ),
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="num_samples",
            default=0,
        ),
        FieldMapping(
            cache_attr="samples",
            default=[],
        ),
        FieldMapping(
            cache_attr="start_time",
        ),
        FieldMapping(
            cache_attr="summary.iops",
        ),
        FieldMapping(
            cache_attr="summary.performance_capacity",
        ),
        FieldMapping(
            cache_attr="summary.utilization_percent",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumAggregateMetricsSampleResponse", AIQUMAGGREGATEMETRICSSAMPLERESPONSE_MAPPING
)
