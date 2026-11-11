"""OntapStoragePool type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.pools.model import (
    OntapStoragePool,
    OntapStoragePoolCapacityDisk,
    OntapStoragePoolCapacitySpareAllocationUnit,
    OntapStoragePoolCapacityUsedAllocationUnit,
    OntapStoragePoolHealthUnhealthyReasonArgument,
    OntapStoragePoolNode,
)

ONTAPSTORAGEPOOL_MAPPING = TypeMapping(
    name="OntapStoragePool",
    model_class=OntapStoragePool,
    api_endpoint="/storage/pools?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="capacity.disk_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity.disks",
            item_model=OntapStoragePoolCapacityDisk,
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity.remaining",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity.spare_allocation_units",
            item_model=OntapStoragePoolCapacitySpareAllocationUnit,
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity.used_allocation_units",
            item_model=OntapStoragePoolCapacityUsedAllocationUnit,
            default=[],
        ),
        FieldMapping(
            cache_attr="health.is_healthy",
            default=False,
        ),
        FieldMapping(
            cache_attr="health.state",
        ),
        FieldMapping(
            cache_attr="health.unhealthy_reason.arguments",
            item_model=OntapStoragePoolHealthUnhealthyReasonArgument,
            default=[],
        ),
        FieldMapping(
            cache_attr="health.unhealthy_reason.code",
        ),
        FieldMapping(
            cache_attr="health.unhealthy_reason.message",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="nodes",
            item_model=OntapStoragePoolNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="storage_type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapStoragePool", ONTAPSTORAGEPOOL_MAPPING)
