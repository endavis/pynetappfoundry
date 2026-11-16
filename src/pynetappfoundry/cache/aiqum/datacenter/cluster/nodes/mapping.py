"""AiqumNode type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.cluster.nodes.model import (
    AiqumNode,
    AiqumNodeHaPartner,
)

AIQUMNODE_MAPPING = TypeMapping(
    name="AiqumNode",
    model_class=AiqumNode,
    api_endpoint="/datacenter/cluster/nodes",
    api_type="aiqum",
    identifier_field="key",
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
            cache_attr="ha.partners",
            item_model=AiqumNodeHaPartner,
            default=[],
        ),
        FieldMapping(
            cache_attr="health",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="performance_capacity.used",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="system_id",
        ),
        FieldMapping(
            cache_attr="uptime",
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

model_registry.register_mapping("AiqumNode", AIQUMNODE_MAPPING)
