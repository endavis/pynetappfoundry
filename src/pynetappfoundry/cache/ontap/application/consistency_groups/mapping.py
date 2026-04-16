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
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="application.component_type",
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
            default=False,
        ),
        FieldMapping(
            cache_attr="clone.parent_consistency_group.name",
        ),
        FieldMapping(
            cache_attr="clone.parent_consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="clone.parent_snapshot.name",
        ),
        FieldMapping(
            cache_attr="clone.parent_snapshot.uuid",
        ),
        FieldMapping(
            cache_attr="clone.parent_svm.name",
        ),
        FieldMapping(
            cache_attr="clone.parent_svm.uuid",
        ),
        FieldMapping(
            cache_attr="clone.split_complete_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="clone.split_estimate",
            default=0,
        ),
        FieldMapping(
            cache_attr="clone.split_initiated",
            default=False,
        ),
        FieldMapping(
            cache_attr="clone.volume.prefix",
        ),
        FieldMapping(
            cache_attr="clone.volume.suffix",
        ),
        FieldMapping(
            cache_attr="consistency_groups",
            transform=_transform_consistency_groups,
            default=[],
        ),
        FieldMapping(
            cache_attr="luns",
            transform=_transform_luns,
            default=[],
        ),
        FieldMapping(
            cache_attr="metric.available_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.iops.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.iops.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.iops.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.iops.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.latency.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.throughput.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.used_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="namespaces",
            transform=_transform_namespaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="parent_consistency_group.name",
        ),
        FieldMapping(
            cache_attr="parent_consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="provisioning_options.action",
        ),
        FieldMapping(
            cache_attr="provisioning_options.name",
        ),
        FieldMapping(
            cache_attr="provisioning_options.storage_service.name",
        ),
        FieldMapping(
            cache_attr="qos.policy.name",
        ),
        FieldMapping(
            cache_attr="qos.policy.uuid",
        ),
        FieldMapping(
            cache_attr="replicated",
            default=False,
        ),
        FieldMapping(
            cache_attr="replication_relationships",
            transform=_transform_replication_relationships,
            default=[],
        ),
        FieldMapping(
            cache_attr="replication_source",
            default=False,
        ),
        FieldMapping(
            cache_attr="restore_to.snapshot.name",
        ),
        FieldMapping(
            cache_attr="restore_to.snapshot.uuid",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="space.available",
            cache_strategy="realtime",
            default=0,
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
            cache_attr="statistics.available_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics.used_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="tiering.control",
        ),
        FieldMapping(
            cache_attr="tiering.object_stores",
            transform=_transform_tiering_object_stores,
            default=[],
        ),
        FieldMapping(
            cache_attr="tiering.policy",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volumes",
            transform=_transform_volumes,
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "OntapConsistencyGroupResponse", ONTAPCONSISTENCYGROUPRESPONSE_MAPPING
)
