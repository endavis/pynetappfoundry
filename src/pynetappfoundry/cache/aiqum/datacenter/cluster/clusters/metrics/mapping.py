"""AiqumClusterMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.cluster.clusters.metrics.model import (
    AiqumClusterMetricsSampleResponse,
)

AIQUMCLUSTERMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumClusterMetricsSampleResponse",
    model_class=AiqumClusterMetricsSampleResponse,
    api_endpoint="/datacenter/cluster/clusters/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumCluster",
    parent_id_field="key",
    fields=(
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
    ),
)

model_registry.register_mapping(
    "AiqumClusterMetricsSampleResponse", AIQUMCLUSTERMETRICSSAMPLERESPONSE_MAPPING
)
