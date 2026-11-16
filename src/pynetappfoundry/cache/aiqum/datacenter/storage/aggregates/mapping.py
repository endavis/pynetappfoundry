"""AiqumAggregate type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.aggregates.model import AiqumAggregate

AIQUMAGGREGATE_MAPPING = TypeMapping(
    name="AiqumAggregate",
    model_class=AiqumAggregate,
    api_endpoint="/datacenter/storage/aggregates",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="block_storage.hybrid_cache.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="block_storage.hybrid_cache.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.mirror.state",
        ),
        FieldMapping(
            cache_attr="block_storage.primary.raid_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.primary.raid_type",
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
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="data_encryption.software_encryption_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
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
            cache_attr="performance_capacity.used",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="snaplock_type",
        ),
        FieldMapping(
            cache_attr="space.block_storage.available",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.block_storage.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.block_storage.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.efficiency.logical_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.efficiency.savings",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumAggregate", AIQUMAGGREGATE_MAPPING)
