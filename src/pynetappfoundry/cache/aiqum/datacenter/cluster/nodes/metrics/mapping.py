"""AiqumNodeMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.cluster.nodes.metrics.model import (
    AiqumNodeMetricsSampleResponse,
)

AIQUMNODEMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumNodeMetricsSampleResponse",
    model_class=AiqumNodeMetricsSampleResponse,
    api_endpoint="/datacenter/cluster/nodes/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumNode",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
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
            cache_attr="summary.latency",
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
    "AiqumNodeMetricsSampleResponse", AIQUMNODEMETRICSSAMPLERESPONSE_MAPPING
)
