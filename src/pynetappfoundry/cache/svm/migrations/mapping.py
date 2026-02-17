# ruff: noqa: E501
"""OntapSvmMigration type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.svm.migrations.model import (
    OntapSvmMigration,
    OntapSvmMigrationAggregate,
    OntapSvmMigrationIpInterface,
    OntapSvmMigrationMessage,
    OntapSvmMigrationVolumeAggregatePair,
)


def _transform_destination_volume_placement_aggregates(
    record: dict[str, Any],
) -> list[OntapSvmMigrationAggregate]:
    """Transform destination.volume_placement.aggregates into OntapSvmMigrationAggregate list."""
    return [
        OntapSvmMigrationAggregate(**item)
        for item in record.get("destination.volume_placement.aggregates", [])
    ]


def _transform_destination_volume_placement_volume_aggregate_pairs(
    record: dict[str, Any],
) -> list[OntapSvmMigrationVolumeAggregatePair]:
    """Transform destination.volume_placement.volume_aggregate_pairs into OntapSvmMigrationVolumeAggregatePair list."""
    return [
        OntapSvmMigrationVolumeAggregatePair(**item)
        for item in record.get("destination.volume_placement.volume_aggregate_pairs", [])
    ]


def _transform_ip_interface_placement_ip_interfaces(
    record: dict[str, Any],
) -> list[OntapSvmMigrationIpInterface]:
    """Transform ip_interface_placement.ip_interfaces into OntapSvmMigrationIpInterface list."""
    return [
        OntapSvmMigrationIpInterface(**item)
        for item in record.get("ip_interface_placement.ip_interfaces", [])
    ]


def _transform_messages(record: dict[str, Any]) -> list[OntapSvmMigrationMessage]:
    """Transform messages into OntapSvmMigrationMessage list."""
    return [OntapSvmMigrationMessage(**item) for item in record.get("messages", [])]


ONTAPSVMMIGRATION_MAPPING = TypeMapping(
    name="OntapSvmMigration",
    model_class=OntapSvmMigration,
    api_endpoint="/svm/migrations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="auto_cutover",
            api_path="auto_cutover",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_source_cleanup",
            api_path="auto_source_cleanup",
            default=False,
        ),
        FieldMapping(
            cache_attr="check_only",
            api_path="check_only",
            default=False,
        ),
        FieldMapping(
            cache_attr="current_operation",
            api_path="current_operation",
        ),
        FieldMapping(
            cache_attr="destination_ipspace_name",
            api_path="destination.ipspace.name",
        ),
        FieldMapping(
            cache_attr="destination_ipspace_uuid",
            api_path="destination.ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="destination_volume_placement_aggregates",
            transform=_transform_destination_volume_placement_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="destination_volume_placement_volume_aggregate_pairs",
            transform=_transform_destination_volume_placement_volume_aggregate_pairs,
            default=[],
        ),
        FieldMapping(
            cache_attr="ip_interface_placement_ip_interfaces",
            transform=_transform_ip_interface_placement_ip_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="last_failed_state",
            api_path="last_failed_state",
        ),
        FieldMapping(
            cache_attr="last_operation",
            api_path="last_operation",
        ),
        FieldMapping(
            cache_attr="messages",
            transform=_transform_messages,
            default=[],
        ),
        FieldMapping(
            cache_attr="point_of_no_return",
            api_path="point_of_no_return",
            default=False,
        ),
        FieldMapping(
            cache_attr="restart_count",
            api_path="restart_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="source_cluster_name",
            api_path="source.cluster.name",
        ),
        FieldMapping(
            cache_attr="source_cluster_uuid",
            api_path="source.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="source_svm_name",
            api_path="source.svm.name",
        ),
        FieldMapping(
            cache_attr="source_svm_uuid",
            api_path="source.svm.uuid",
        ),
        FieldMapping(
            cache_attr="throttle",
            api_path="throttle",
            default=0,
        ),
        FieldMapping(
            cache_attr="time_metrics_cutover_complete_time",
            api_path="time_metrics.cutover_complete_time",
        ),
        FieldMapping(
            cache_attr="time_metrics_cutover_start_time",
            api_path="time_metrics.cutover_start_time",
        ),
        FieldMapping(
            cache_attr="time_metrics_cutover_trigger_time",
            api_path="time_metrics.cutover_trigger_time",
        ),
        FieldMapping(
            cache_attr="time_metrics_end_time",
            api_path="time_metrics.end_time",
        ),
        FieldMapping(
            cache_attr="time_metrics_last_pause_time",
            api_path="time_metrics.last_pause_time",
        ),
        FieldMapping(
            cache_attr="time_metrics_last_resume_time",
            api_path="time_metrics.last_resume_time",
        ),
        FieldMapping(
            cache_attr="time_metrics_start_time",
            api_path="time_metrics.start_time",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmMigration", ONTAPSVMMIGRATION_MAPPING)
