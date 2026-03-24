# ruff: noqa: E501
"""OntapConsistencyGroupResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.application.consistency_groups.model import (
    OntapConsistencyGroupResponse,
    OntapConsistencyGroupResponseConsistencyGroup,
    OntapConsistencyGroupResponseLun,
    OntapConsistencyGroupResponseNamespace,
    OntapConsistencyGroupResponseObjectStore,
    OntapConsistencyGroupResponseReplicationRelationship,
    OntapConsistencyGroupResponseVolume,
)


def _transform_consistency_groups(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupResponseConsistencyGroup]:
    """Transform consistency_groups into OntapConsistencyGroupResponseConsistencyGroup list."""
    return [
        OntapConsistencyGroupResponseConsistencyGroup(**item)
        for item in record.get("consistency_groups", [])
    ]


def _transform_luns(record: dict[str, Any]) -> list[OntapConsistencyGroupResponseLun]:
    """Transform luns into OntapConsistencyGroupResponseLun list."""
    return [OntapConsistencyGroupResponseLun(**item) for item in record.get("luns", [])]


def _transform_namespaces(record: dict[str, Any]) -> list[OntapConsistencyGroupResponseNamespace]:
    """Transform namespaces into OntapConsistencyGroupResponseNamespace list."""
    return [OntapConsistencyGroupResponseNamespace(**item) for item in record.get("namespaces", [])]


def _transform_replication_relationships(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupResponseReplicationRelationship]:
    """Transform replication_relationships into OntapConsistencyGroupResponseReplicationRelationship list."""
    return [
        OntapConsistencyGroupResponseReplicationRelationship(**item)
        for item in record.get("replication_relationships", [])
    ]


def _transform_tiering_object_stores(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupResponseObjectStore]:
    """Transform tiering.object_stores into OntapConsistencyGroupResponseObjectStore list."""
    return [
        OntapConsistencyGroupResponseObjectStore(**item)
        for item in record.get("tiering.object_stores", [])
    ]


def _transform_volumes(record: dict[str, Any]) -> list[OntapConsistencyGroupResponseVolume]:
    """Transform volumes into OntapConsistencyGroupResponseVolume list."""
    return [OntapConsistencyGroupResponseVolume(**item) for item in record.get("volumes", [])]


ONTAPCONSISTENCYGROUPRESPONSE_MAPPING = TypeMapping(
    name="OntapConsistencyGroupResponse",
    model_class=OntapConsistencyGroupResponse,
    api_endpoint="/application/consistency-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="application_component_type",
            api_path="application.component_type",
        ),
        FieldMapping(
            cache_attr="application_type",
            api_path="application.type",
        ),
        FieldMapping(
            cache_attr="clone_guarantee_type",
            api_path="clone.guarantee.type",
        ),
        FieldMapping(
            cache_attr="clone_is_flexclone",
            api_path="clone.is_flexclone",
            default=False,
        ),
        FieldMapping(
            cache_attr="clone_parent_consistency_group_name",
            api_path="clone.parent_consistency_group.name",
        ),
        FieldMapping(
            cache_attr="clone_parent_consistency_group_uuid",
            api_path="clone.parent_consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="clone_parent_snapshot_name",
            api_path="clone.parent_snapshot.name",
        ),
        FieldMapping(
            cache_attr="clone_parent_snapshot_uuid",
            api_path="clone.parent_snapshot.uuid",
        ),
        FieldMapping(
            cache_attr="clone_parent_svm_name",
            api_path="clone.parent_svm.name",
        ),
        FieldMapping(
            cache_attr="clone_parent_svm_uuid",
            api_path="clone.parent_svm.uuid",
        ),
        FieldMapping(
            cache_attr="clone_split_complete_percent",
            api_path="clone.split_complete_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="clone_split_estimate",
            api_path="clone.split_estimate",
            default=0,
        ),
        FieldMapping(
            cache_attr="clone_split_initiated",
            api_path="clone.split_initiated",
            default=False,
        ),
        FieldMapping(
            cache_attr="clone_volume_prefix",
            api_path="clone.volume.prefix",
        ),
        FieldMapping(
            cache_attr="clone_volume_suffix",
            api_path="clone.volume.suffix",
        ),
        FieldMapping(
            cache_attr="consistency_groups",
            api_path="consistency_groups",
            transform=_transform_consistency_groups,
            default=[],
        ),
        FieldMapping(
            cache_attr="luns",
            api_path="luns",
            transform=_transform_luns,
            default=[],
        ),
        FieldMapping(
            cache_attr="metric_available_space",
            api_path="metric.available_space",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_duration",
            api_path="metric.duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_iops_other",
            api_path="metric.iops.other",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_iops_read",
            api_path="metric.iops.read",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_iops_total",
            api_path="metric.iops.total",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_iops_write",
            api_path="metric.iops.write",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_latency_other",
            api_path="metric.latency.other",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_latency_read",
            api_path="metric.latency.read",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_latency_total",
            api_path="metric.latency.total",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_latency_write",
            api_path="metric.latency.write",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_size",
            api_path="metric.size",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_status",
            api_path="metric.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_throughput_other",
            api_path="metric.throughput.other",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_throughput_read",
            api_path="metric.throughput.read",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_throughput_total",
            api_path="metric.throughput.total",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_throughput_write",
            api_path="metric.throughput.write",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_timestamp",
            api_path="metric.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric_used_space",
            api_path="metric.used_space",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="namespaces",
            api_path="namespaces",
            transform=_transform_namespaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="parent_consistency_group_name",
            api_path="parent_consistency_group.name",
        ),
        FieldMapping(
            cache_attr="parent_consistency_group_uuid",
            api_path="parent_consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="provisioning_options_action",
            api_path="provisioning_options.action",
        ),
        FieldMapping(
            cache_attr="provisioning_options_name",
            api_path="provisioning_options.name",
        ),
        FieldMapping(
            cache_attr="provisioning_options_storage_service_name",
            api_path="provisioning_options.storage_service.name",
        ),
        FieldMapping(
            cache_attr="qos_policy_name",
            api_path="qos.policy.name",
        ),
        FieldMapping(
            cache_attr="qos_policy_uuid",
            api_path="qos.policy.uuid",
        ),
        FieldMapping(
            cache_attr="replicated",
            api_path="replicated",
            default=False,
        ),
        FieldMapping(
            cache_attr="replication_relationships",
            api_path="replication_relationships",
            transform=_transform_replication_relationships,
            default=[],
        ),
        FieldMapping(
            cache_attr="replication_source",
            api_path="replication_source",
            default=False,
        ),
        FieldMapping(
            cache_attr="restore_to_snapshot_name",
            api_path="restore_to.snapshot.name",
        ),
        FieldMapping(
            cache_attr="restore_to_snapshot_uuid",
            api_path="restore_to.snapshot.uuid",
        ),
        FieldMapping(
            cache_attr="snapshot_policy_name",
            api_path="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy_uuid",
            api_path="snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="space_available",
            api_path="space.available",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="space_size",
            api_path="space.size",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="space_used",
            api_path="space.used",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_available_space",
            api_path="statistics.available_space",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_iops_raw_other",
            api_path="statistics.iops_raw.other",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_iops_raw_read",
            api_path="statistics.iops_raw.read",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_iops_raw_total",
            api_path="statistics.iops_raw.total",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_iops_raw_write",
            api_path="statistics.iops_raw.write",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_latency_raw_other",
            api_path="statistics.latency_raw.other",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_latency_raw_read",
            api_path="statistics.latency_raw.read",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_latency_raw_total",
            api_path="statistics.latency_raw.total",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_latency_raw_write",
            api_path="statistics.latency_raw.write",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_size",
            api_path="statistics.size",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_status",
            api_path="statistics.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_other",
            api_path="statistics.throughput_raw.other",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_read",
            api_path="statistics.throughput_raw.read",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_total",
            api_path="statistics.throughput_raw.total",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_write",
            api_path="statistics.throughput_raw.write",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_timestamp",
            api_path="statistics.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics_used_space",
            api_path="statistics.used_space",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="tiering_control",
            api_path="tiering.control",
        ),
        FieldMapping(
            cache_attr="tiering_object_stores",
            api_path="tiering.object_stores",
            transform=_transform_tiering_object_stores,
            default=[],
        ),
        FieldMapping(
            cache_attr="tiering_policy",
            api_path="tiering.policy",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volumes",
            api_path="volumes",
            transform=_transform_volumes,
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "OntapConsistencyGroupResponse", ONTAPCONSISTENCYGROUPRESPONSE_MAPPING
)
