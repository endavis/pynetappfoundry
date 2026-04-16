# ruff: noqa: E501
"""OntapLun type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.luns.model import (
    OntapLun,
    OntapLunAttribute,
    OntapLunCopyDestination,
    OntapLunCopySourceProgressFailureArgument,
    OntapLunLunMap,
    OntapLunMovementProgressFailureArgument,
    OntapLunProvisioningOptionsTieringObjectStore,
    OntapLunVvolBinding,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_attributes(record: dict[str, Any]) -> list[OntapLunAttribute]:
    """Transform attributes into OntapLunAttribute list."""
    return [OntapLunAttribute(**item) for item in record.get("attributes", [])]


def _transform_copy_destinations(record: dict[str, Any]) -> list[OntapLunCopyDestination]:
    """Transform copy.destinations into OntapLunCopyDestination list."""
    try:
        items = get_nested_value(record, "copy.destinations")
    except Exception:
        items = []
    return [OntapLunCopyDestination(**item) for item in items]


def _transform_copy_source_progress_failure_arguments(
    record: dict[str, Any],
) -> list[OntapLunCopySourceProgressFailureArgument]:
    """Transform copy.source.progress.failure.arguments into OntapLunCopySourceProgressFailureArgument list."""
    try:
        items = get_nested_value(record, "copy.source.progress.failure.arguments")
    except Exception:
        items = []
    return [OntapLunCopySourceProgressFailureArgument(**item) for item in items]


def _transform_lun_maps(record: dict[str, Any]) -> list[OntapLunLunMap]:
    """Transform lun_maps into OntapLunLunMap list."""
    return [OntapLunLunMap(**item) for item in record.get("lun_maps", [])]


def _transform_movement_progress_failure_arguments(
    record: dict[str, Any],
) -> list[OntapLunMovementProgressFailureArgument]:
    """Transform movement.progress.failure.arguments into OntapLunMovementProgressFailureArgument list."""
    try:
        items = get_nested_value(record, "movement.progress.failure.arguments")
    except Exception:
        items = []
    return [OntapLunMovementProgressFailureArgument(**item) for item in items]


def _transform_provisioning_options_tiering_object_stores(
    record: dict[str, Any],
) -> list[OntapLunProvisioningOptionsTieringObjectStore]:
    """Transform provisioning_options.tiering.object_stores into OntapLunProvisioningOptionsTieringObjectStore list."""
    try:
        items = get_nested_value(record, "provisioning_options.tiering.object_stores")
    except Exception:
        items = []
    return [OntapLunProvisioningOptionsTieringObjectStore(**item) for item in items]


def _transform_vvol_bindings(record: dict[str, Any]) -> list[OntapLunVvolBinding]:
    """Transform vvol.bindings into OntapLunVvolBinding list."""
    try:
        items = get_nested_value(record, "vvol.bindings")
    except Exception:
        items = []
    return [OntapLunVvolBinding(**item) for item in items]


ONTAPLUN_MAPPING = TypeMapping(
    name="OntapLun",
    model_class=OntapLun,
    api_endpoint="/storage/luns?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="attributes",
            transform=_transform_attributes,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="auto_delete",
            default=False,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="class_",
            api_path="class",
        ),
        FieldMapping(
            cache_attr="clone.source.name",
        ),
        FieldMapping(
            cache_attr="clone.source.uuid",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="consistency_group.name",
        ),
        FieldMapping(
            cache_attr="consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="convert.namespace.name",
        ),
        FieldMapping(
            cache_attr="convert.namespace.uuid",
        ),
        FieldMapping(
            cache_attr="copy_.destinations",
            api_path="copy.destinations",
            transform=_transform_copy_destinations,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.max_throughput",
            api_path="copy.source.max_throughput",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.name",
            api_path="copy.source.name",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.peer.name",
            api_path="copy.source.peer.name",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.peer.uuid",
            api_path="copy.source.peer.uuid",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.elapsed",
            api_path="copy.source.progress.elapsed",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.failure.arguments",
            api_path="copy.source.progress.failure.arguments",
            transform=_transform_copy_source_progress_failure_arguments,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.failure.code",
            api_path="copy.source.progress.failure.code",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.failure.message",
            api_path="copy.source.progress.failure.message",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.percent_complete",
            api_path="copy.source.progress.percent_complete",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.state",
            api_path="copy.source.progress.state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.progress.volume_snapshot_blocked",
            api_path="copy.source.progress.volume_snapshot_blocked",
            default=False,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="copy_.source.uuid",
            api_path="copy.source.uuid",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="location.logical_unit",
        ),
        FieldMapping(
            cache_attr="location.node.name",
        ),
        FieldMapping(
            cache_attr="location.node.uuid",
        ),
        FieldMapping(
            cache_attr="location.qtree.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="location.qtree.name",
        ),
        FieldMapping(
            cache_attr="location.volume.name",
        ),
        FieldMapping(
            cache_attr="location.volume.uuid",
        ),
        FieldMapping(
            cache_attr="lun_maps",
            transform=_transform_lun_maps,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.duration",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.iops.other",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.iops.read",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.iops.total",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.iops.write",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.latency.other",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.latency.read",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.latency.total",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.latency.write",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.status",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.throughput.other",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.throughput.read",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.throughput.total",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.throughput.write",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.timestamp",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.max_throughput",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.paths.destination",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.paths.source",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.elapsed",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.failure.arguments",
            transform=_transform_movement_progress_failure_arguments,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.failure.code",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.failure.message",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.percent_complete",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="movement.progress.volume_snapshot_blocked",
            default=False,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="os_type",
        ),
        FieldMapping(
            cache_attr="provisioning_options.auto",
            default=False,
        ),
        FieldMapping(
            cache_attr="provisioning_options.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="provisioning_options.qos_policy.name",
        ),
        FieldMapping(
            cache_attr="provisioning_options.qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="provisioning_options.snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="provisioning_options.snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="provisioning_options.storage_service.name",
        ),
        FieldMapping(
            cache_attr="provisioning_options.tiering.control",
        ),
        FieldMapping(
            cache_attr="provisioning_options.tiering.object_stores",
            transform=_transform_provisioning_options_tiering_object_stores,
            default=[],
        ),
        FieldMapping(
            cache_attr="provisioning_options.tiering.policy",
        ),
        FieldMapping(
            cache_attr="provisioning_options.use_mirrored_aggregates",
            default=False,
        ),
        FieldMapping(
            cache_attr="qos_policy.name",
        ),
        FieldMapping(
            cache_attr="qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="space.efficiency_ratio",
            cache_strategy="realtime",
            default=0.0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="space.guarantee.requested",
            cache_strategy="realtime",
            default=False,
        ),
        FieldMapping(
            cache_attr="space.guarantee.reserved",
            cache_strategy="realtime",
            default=False,
        ),
        FieldMapping(
            cache_attr="space.physical_used",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="space.physical_used_by_snapshots",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="space.scsi_thin_provisioning_support_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="space.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.other",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.read",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.total",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.write",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.other",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.read",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.total",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.write",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.status",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.other",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.read",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.total",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.write",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.timestamp",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="status.container_state",
        ),
        FieldMapping(
            cache_attr="status.mapped",
            default=False,
        ),
        FieldMapping(
            cache_attr="status.read_only",
            default=False,
        ),
        FieldMapping(
            cache_attr="status.state",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vvol.bindings",
            transform=_transform_vvol_bindings,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="vvol.is_bound",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapLun", ONTAPLUN_MAPPING)
