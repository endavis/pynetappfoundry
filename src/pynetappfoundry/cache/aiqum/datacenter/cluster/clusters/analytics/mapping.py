"""AiqumClusterAnalytics type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.cluster.clusters.analytics.model import (
    AiqumClusterAnalytics,
)

AIQUMCLUSTERANALYTICS_MAPPING = TypeMapping(
    name="AiqumClusterAnalytics",
    model_class=AiqumClusterAnalytics,
    api_endpoint="/datacenter/cluster/clusters/analytics",
    api_type="aiqum",
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
            cache_attr="iops",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="management_ip",
        ),
        FieldMapping(
            cache_attr="period",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput",
            default=0.0,
        ),
    ),
)

model_registry.register_mapping("AiqumClusterAnalytics", AIQUMCLUSTERANALYTICS_MAPPING)
