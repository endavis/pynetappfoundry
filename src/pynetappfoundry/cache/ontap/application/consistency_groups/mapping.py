# ruff: noqa: E501
"""OntapConsistencyGroupResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.consistency_groups.model import (
    OntapConsistencyGroupResponse,
    OntapConsistencyGroupResponseConsistencyGroup,
    OntapConsistencyGroupResponseLun,
    OntapConsistencyGroupResponseNamespace,
    OntapConsistencyGroupResponseReplicationRelationship,
    OntapConsistencyGroupResponseTieringObjectStore,
    OntapConsistencyGroupResponseVolume,
)
from pynetappfoundry.utils.dict_path import get_nested_value


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
) -> list[OntapConsistencyGroupResponseTieringObjectStore]:
    """Transform tiering.object_stores into OntapConsistencyGroupResponseTieringObjectStore list."""
    try:
        items = get_nested_value(record, "tiering.object_stores")
    except Exception:
        items = []
    return [OntapConsistencyGroupResponseTieringObjectStore(**item) for item in items]


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
            cache_attr="application.component_type",
            api_path="application.component_type",
        ),
        FieldMapping(
            cache_attr="application.type_",
            api_path="application.type",
        ),
        FieldMapping(
            cache_attr="clone.guarantee.type_",
            api_path="clone.guarantee.type",
        ),
        FieldMapping(
            cache_attr="clone.is_flexclone",
            api_path="clone.is_flexclone",
            default=False,
        ),
        FieldMapping(
            cache_attr="clone.parent_consistency_group.name",
            api_path="clone.parent_consistency_group.name",
        ),
        FieldMapping(
            cache_attr="clone.parent_consistency_group.uuid",
            api_path="clone.parent_consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="clone.parent_snapshot.name",
            api_path="clone.parent_snapshot.name",
        ),
        FieldMapping(
            cache_attr="clone.parent_snapshot.uuid",
            api_path="clone.parent_snapshot.uuid",
        ),
        FieldMapping(
            cache_attr="clone.parent_svm.name",
            api_path="clone.parent_svm.name",
        ),
        FieldMapping(
            cache_attr="clone.parent_svm.uuid",
            api_path="clone.parent_svm.uuid",
        ),
        FieldMapping(
            cache_attr="clone.split_complete_percent",
            api_path="clone.split_complete_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="clone.split_estimate",
            api_path="clone.split_estimate",
            default=0,
        ),
        FieldMapping(
            cache_attr="clone.split_initiated",
            api_path="clone.split_initiated",
            default=False,
        ),
        FieldMapping(
            cache_attr="clone.volume.prefix",
            api_path="clone.volume.prefix",
        ),
        FieldMapping(
            cache_attr="clone.volume.suffix",
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
            cache_attr="metric.available_space",
            api_path="metric.available_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.duration",
            api_path="metric.duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.iops.other",
            api_path="metric.iops.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.iops.read",
            api_path="metric.iops.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.iops.total",
            api_path="metric.iops.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.iops.write",
            api_path="metric.iops.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.other",
            api_path="metric.latency.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.read",
            api_path="metric.latency.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.total",
            api_path="metric.latency.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.write",
            api_path="metric.latency.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.size",
            api_path="metric.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.status",
            api_path="metric.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.throughput.other",
            api_path="metric.throughput.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.read",
            api_path="metric.throughput.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.total",
            api_path="metric.throughput.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.write",
            api_path="metric.throughput.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.timestamp",
            api_path="metric.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.used_space",
            api_path="metric.used_space",
            cache_strategy="realtime",
            default=0,
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
            cache_attr="parent_consistency_group.name",
            api_path="parent_consistency_group.name",
        ),
        FieldMapping(
            cache_attr="parent_consistency_group.uuid",
            api_path="parent_consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="provisioning_options.action",
            api_path="provisioning_options.action",
        ),
        FieldMapping(
            cache_attr="provisioning_options.name",
            api_path="provisioning_options.name",
        ),
        FieldMapping(
            cache_attr="provisioning_options.storage_service.name",
            api_path="provisioning_options.storage_service.name",
        ),
        FieldMapping(
            cache_attr="qos.policy.name",
            api_path="qos.policy.name",
        ),
        FieldMapping(
            cache_attr="qos.policy.uuid",
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
            cache_attr="restore_to.snapshot.name",
            api_path="restore_to.snapshot.name",
        ),
        FieldMapping(
            cache_attr="restore_to.snapshot.uuid",
            api_path="restore_to.snapshot.uuid",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.name",
            api_path="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.uuid",
            api_path="snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="space.available",
            api_path="space.available",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.size",
            api_path="space.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used",
            api_path="space.used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.available_space",
            api_path="statistics.available_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.other",
            api_path="statistics.iops_raw.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.read",
            api_path="statistics.iops_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.total",
            api_path="statistics.iops_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.write",
            api_path="statistics.iops_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.other",
            api_path="statistics.latency_raw.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.read",
            api_path="statistics.latency_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.total",
            api_path="statistics.latency_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.write",
            api_path="statistics.latency_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.size",
            api_path="statistics.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.status",
            api_path="statistics.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.other",
            api_path="statistics.throughput_raw.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.read",
            api_path="statistics.throughput_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.total",
            api_path="statistics.throughput_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.write",
            api_path="statistics.throughput_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.timestamp",
            api_path="statistics.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics.used_space",
            api_path="statistics.used_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="tiering.control",
            api_path="tiering.control",
        ),
        FieldMapping(
            cache_attr="tiering.object_stores",
            api_path="tiering.object_stores",
            transform=_transform_tiering_object_stores,
            default=[],
        ),
        FieldMapping(
            cache_attr="tiering.policy",
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
