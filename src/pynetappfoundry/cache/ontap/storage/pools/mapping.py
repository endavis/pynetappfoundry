"""OntapStoragePool type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.pools.model import (
    OntapStoragePool,
    OntapStoragePoolArgument,
    OntapStoragePoolDisk,
    OntapStoragePoolNode,
    OntapStoragePoolSpareAllocationUnit,
    OntapStoragePoolUsedAllocationUnit,
)


def _transform_capacity_disks(record: dict[str, Any]) -> list[OntapStoragePoolDisk]:
    """Transform capacity.disks into OntapStoragePoolDisk list."""
    return [OntapStoragePoolDisk(**item) for item in record.get("capacity.disks", [])]


def _transform_capacity_spare_allocation_units(
    record: dict[str, Any],
) -> list[OntapStoragePoolSpareAllocationUnit]:
    """Transform capacity.spare_allocation_units into OntapStoragePoolSpareAllocationUnit list."""
    return [
        OntapStoragePoolSpareAllocationUnit(**item)
        for item in record.get("capacity.spare_allocation_units", [])
    ]


def _transform_capacity_used_allocation_units(
    record: dict[str, Any],
) -> list[OntapStoragePoolUsedAllocationUnit]:
    """Transform capacity.used_allocation_units into OntapStoragePoolUsedAllocationUnit list."""
    return [
        OntapStoragePoolUsedAllocationUnit(**item)
        for item in record.get("capacity.used_allocation_units", [])
    ]


def _transform_health_unhealthy_reason_arguments(
    record: dict[str, Any],
) -> list[OntapStoragePoolArgument]:
    """Transform health.unhealthy_reason.arguments into OntapStoragePoolArgument list."""
    return [
        OntapStoragePoolArgument(**item)
        for item in record.get("health.unhealthy_reason.arguments", [])
    ]


def _transform_nodes(record: dict[str, Any]) -> list[OntapStoragePoolNode]:
    """Transform nodes into OntapStoragePoolNode list."""
    return [OntapStoragePoolNode(**item) for item in record.get("nodes", [])]


ONTAPSTORAGEPOOL_MAPPING = TypeMapping(
    name="OntapStoragePool",
    model_class=OntapStoragePool,
    api_endpoint="/storage/pools?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="capacity_disk_count",
            api_path="capacity.disk_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity_disks",
            api_path="capacity.disks",
            transform=_transform_capacity_disks,
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity_remaining",
            api_path="capacity.remaining",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity_spare_allocation_units",
            api_path="capacity.spare_allocation_units",
            transform=_transform_capacity_spare_allocation_units,
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity_total",
            api_path="capacity.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity_used_allocation_units",
            api_path="capacity.used_allocation_units",
            transform=_transform_capacity_used_allocation_units,
            default=[],
        ),
        FieldMapping(
            cache_attr="health_is_healthy",
            api_path="health.is_healthy",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_state",
            api_path="health.state",
        ),
        FieldMapping(
            cache_attr="health_unhealthy_reason_arguments",
            api_path="health.unhealthy_reason.arguments",
            transform=_transform_health_unhealthy_reason_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="health_unhealthy_reason_code",
            api_path="health.unhealthy_reason.code",
        ),
        FieldMapping(
            cache_attr="health_unhealthy_reason_message",
            api_path="health.unhealthy_reason.message",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="nodes",
            api_path="nodes",
            transform=_transform_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="storage_type",
            api_path="storage_type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapStoragePool", ONTAPSTORAGEPOOL_MAPPING)
