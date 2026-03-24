"""OntapDisk type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.disks.model import (
    OntapDisk,
    OntapDiskAggregate,
    OntapDiskArgument,
    OntapDiskError,
    OntapDiskPath,
)


def _transform_aggregates(record: dict[str, Any]) -> list[OntapDiskAggregate]:
    """Transform aggregates into OntapDiskAggregate list."""
    return [OntapDiskAggregate(**item) for item in record.get("aggregates", [])]


def _transform_error(record: dict[str, Any]) -> list[OntapDiskError]:
    """Transform error into OntapDiskError list."""
    return [OntapDiskError(**item) for item in record.get("error", [])]


def _transform_outage_reason_arguments(record: dict[str, Any]) -> list[OntapDiskArgument]:
    """Transform outage.reason.arguments into OntapDiskArgument list."""
    return [OntapDiskArgument(**item) for item in record.get("outage.reason.arguments", [])]


def _transform_paths(record: dict[str, Any]) -> list[OntapDiskPath]:
    """Transform paths into OntapDiskPath list."""
    return [OntapDiskPath(**item) for item in record.get("paths", [])]


ONTAPDISK_MAPPING = TypeMapping(
    name="OntapDisk",
    model_class=OntapDisk,
    api_endpoint="/storage/disks?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="aggregates",
            api_path="aggregates",
            transform=_transform_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="bay",
            api_path="bay",
            default=0,
        ),
        FieldMapping(
            cache_attr="bytes_per_sector",
            api_path="bytes_per_sector",
            default=0,
        ),
        FieldMapping(
            cache_attr="class_",
            api_path="class",
        ),
        FieldMapping(
            cache_attr="compliance_standard",
            api_path="compliance_standard",
        ),
        FieldMapping(
            cache_attr="container_type",
            api_path="container_type",
        ),
        FieldMapping(
            cache_attr="control_standard",
            api_path="control_standard",
        ),
        FieldMapping(
            cache_attr="dr_node_name",
            api_path="dr_node.name",
        ),
        FieldMapping(
            cache_attr="dr_node_uuid",
            api_path="dr_node.uuid",
        ),
        FieldMapping(
            cache_attr="drawer_id",
            api_path="drawer.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="drawer_slot",
            api_path="drawer.slot",
            default=0,
        ),
        FieldMapping(
            cache_attr="effective_type",
            api_path="effective_type",
        ),
        FieldMapping(
            cache_attr="encryption_operation",
            api_path="encryption_operation",
        ),
        FieldMapping(
            cache_attr="error",
            api_path="error",
            transform=_transform_error,
            default=[],
        ),
        FieldMapping(
            cache_attr="fips_certified",
            api_path="fips_certified",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware_version",
            api_path="firmware_version",
        ),
        FieldMapping(
            cache_attr="home_node_name",
            api_path="home_node.name",
        ),
        FieldMapping(
            cache_attr="home_node_uuid",
            api_path="home_node.uuid",
        ),
        FieldMapping(
            cache_attr="key_id_data",
            api_path="key_id.data",
        ),
        FieldMapping(
            cache_attr="key_id_fips",
            api_path="key_id.fips",
        ),
        FieldMapping(
            cache_attr="local",
            api_path="local",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="outage_persistently_failed",
            api_path="outage.persistently_failed",
            default=False,
        ),
        FieldMapping(
            cache_attr="outage_reason_arguments",
            api_path="outage.reason.arguments",
            transform=_transform_outage_reason_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="outage_reason_code",
            api_path="outage.reason.code",
        ),
        FieldMapping(
            cache_attr="outage_reason_message",
            api_path="outage.reason.message",
        ),
        FieldMapping(
            cache_attr="overall_security",
            api_path="overall_security",
        ),
        FieldMapping(
            cache_attr="paths",
            api_path="paths",
            transform=_transform_paths,
            default=[],
        ),
        FieldMapping(
            cache_attr="physical_size",
            api_path="physical_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="pool",
            api_path="pool",
        ),
        FieldMapping(
            cache_attr="protection_mode",
            api_path="protection_mode",
        ),
        FieldMapping(
            cache_attr="rated_life_used_percent",
            api_path="rated_life_used_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="right_size_sector_count",
            api_path="right_size_sector_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="rpm",
            api_path="rpm",
            default=0,
        ),
        FieldMapping(
            cache_attr="sanitize_spare",
            api_path="sanitize_spare",
            default=False,
        ),
        FieldMapping(
            cache_attr="sector_count",
            api_path="sector_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="self_encrypting",
            api_path="self_encrypting",
            default=False,
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="shelf_uid",
            api_path="shelf.uid",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="stats_average_latency",
            api_path="stats.average_latency",
            default=0,
        ),
        FieldMapping(
            cache_attr="stats_iops_total",
            api_path="stats.iops_total",
            default=0,
        ),
        FieldMapping(
            cache_attr="stats_path_error_count",
            api_path="stats.path_error_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="stats_power_on_hours",
            api_path="stats.power_on_hours",
            default=0,
        ),
        FieldMapping(
            cache_attr="stats_throughput",
            api_path="stats.throughput",
            default=0,
        ),
        FieldMapping(
            cache_attr="storage_pool_name",
            api_path="storage_pool.name",
        ),
        FieldMapping(
            cache_attr="storage_pool_uuid",
            api_path="storage_pool.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uid",
            api_path="uid",
        ),
        FieldMapping(
            cache_attr="usable_size",
            api_path="usable_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vendor",
            api_path="vendor",
        ),
        FieldMapping(
            cache_attr="virtual_container",
            api_path="virtual.container",
        ),
        FieldMapping(
            cache_attr="virtual_object",
            api_path="virtual.object",
        ),
        FieldMapping(
            cache_attr="virtual_storage_account",
            api_path="virtual.storage_account",
        ),
        FieldMapping(
            cache_attr="virtual_target_address",
            api_path="virtual.target_address",
        ),
    ),
)

model_registry.register_mapping("OntapDisk", ONTAPDISK_MAPPING)
