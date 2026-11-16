"""AiqumAggregateAnalytics type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.aggregates.analytics.model import (
    AiqumAggregateAnalytics,
)

AIQUMAGGREGATEANALYTICS_MAPPING = TypeMapping(
    name="AiqumAggregateAnalytics",
    model_class=AiqumAggregateAnalytics,
    api_endpoint="/datacenter/storage/aggregates/analytics",
    api_type="aiqum",
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
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="iops",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="latency",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="node.key",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="performance_capacity.available_iops",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="performance_capacity.used_percent",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="period",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="utilization_percent",
            default=0.0,
        ),
    ),
)

model_registry.register_mapping("AiqumAggregateAnalytics", AIQUMAGGREGATEANALYTICS_MAPPING)
