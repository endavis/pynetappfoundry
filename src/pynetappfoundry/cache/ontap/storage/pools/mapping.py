# ruff: noqa: E501
"""OntapStoragePool type mapping."""

from __future__ import annotations

from typing import Any

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
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_capacity_disks(record: dict[str, Any]) -> list[OntapStoragePoolCapacityDisk]:
    """Transform capacity.disks into OntapStoragePoolCapacityDisk list."""
    try:
        items = get_nested_value(record, "capacity.disks")
    except Exception:
        items = []
    return [OntapStoragePoolCapacityDisk(**item) for item in items]


def _transform_capacity_spare_allocation_units(
    record: dict[str, Any],
) -> list[OntapStoragePoolCapacitySpareAllocationUnit]:
    """Transform capacity.spare_allocation_units into OntapStoragePoolCapacitySpareAllocationUnit list."""
    try:
        items = get_nested_value(record, "capacity.spare_allocation_units")
    except Exception:
        items = []
    return [OntapStoragePoolCapacitySpareAllocationUnit(**item) for item in items]


def _transform_capacity_used_allocation_units(
    record: dict[str, Any],
) -> list[OntapStoragePoolCapacityUsedAllocationUnit]:
    """Transform capacity.used_allocation_units into OntapStoragePoolCapacityUsedAllocationUnit list."""
    try:
        items = get_nested_value(record, "capacity.used_allocation_units")
    except Exception:
        items = []
    return [OntapStoragePoolCapacityUsedAllocationUnit(**item) for item in items]


def _transform_health_unhealthy_reason_arguments(
    record: dict[str, Any],
) -> list[OntapStoragePoolHealthUnhealthyReasonArgument]:
    """Transform health.unhealthy_reason.arguments into OntapStoragePoolHealthUnhealthyReasonArgument list."""
    try:
        items = get_nested_value(record, "health.unhealthy_reason.arguments")
    except Exception:
        items = []
    return [OntapStoragePoolHealthUnhealthyReasonArgument(**item) for item in items]


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
            cache_attr="capacity.disk_count",
            api_path="capacity.disk_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity.disks",
            api_path="capacity.disks",
            transform=_transform_capacity_disks,
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity.remaining",
            api_path="capacity.remaining",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity.spare_allocation_units",
            api_path="capacity.spare_allocation_units",
            transform=_transform_capacity_spare_allocation_units,
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity.total",
            api_path="capacity.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="capacity.used_allocation_units",
            api_path="capacity.used_allocation_units",
            transform=_transform_capacity_used_allocation_units,
            default=[],
        ),
        FieldMapping(
            cache_attr="health.is_healthy",
            api_path="health.is_healthy",
            default=False,
        ),
        FieldMapping(
            cache_attr="health.state",
            api_path="health.state",
        ),
        FieldMapping(
            cache_attr="health.unhealthy_reason.arguments",
            api_path="health.unhealthy_reason.arguments",
            transform=_transform_health_unhealthy_reason_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="health.unhealthy_reason.code",
            api_path="health.unhealthy_reason.code",
        ),
        FieldMapping(
            cache_attr="health.unhealthy_reason.message",
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
