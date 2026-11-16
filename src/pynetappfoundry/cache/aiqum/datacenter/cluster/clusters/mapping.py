"""AiqumCluster type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.cluster.clusters.model import (
    AiqumCluster,
    AiqumClusterNode,
)

AIQUMCLUSTER_MAPPING = TypeMapping(
    name="AiqumCluster",
    model_class=AiqumCluster,
    api_endpoint="/datacenter/cluster/clusters",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="contact",
        ),
        FieldMapping(
            cache_attr="isSanOptimized",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_san_optimized",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="management_ip",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="nodes",
            item_model=AiqumClusterNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="protocol_breakdown.cifs",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol_breakdown.fcp",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol_breakdown.iscsi",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol_breakdown.nfs",
            default=0,
        ),
        FieldMapping(
            cache_attr="storage_capacity.available",
            default=0,
        ),
        FieldMapping(
            cache_attr="storage_capacity.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="storage_capacity.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="version.full",
        ),
        FieldMapping(
            cache_attr="version.generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.minor",
            default=0,
        ),
    ),
)

model_registry.register_mapping("AiqumCluster", AIQUMCLUSTER_MAPPING)
