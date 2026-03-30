# ruff: noqa: E501
"""OntapConsistencyGroupSnapshotResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.consistency_groups.snapshots.model import (
    OntapConsistencyGroupSnapshotResponse,
    OntapConsistencyGroupSnapshotResponseLun,
    OntapConsistencyGroupSnapshotResponseMissingLun,
    OntapConsistencyGroupSnapshotResponseMissingNamespace,
    OntapConsistencyGroupSnapshotResponseMissingVolume,
    OntapConsistencyGroupSnapshotResponseNamespace,
    OntapConsistencyGroupSnapshotResponseSnapshotVolume,
)


def _transform_luns(record: dict[str, Any]) -> list[OntapConsistencyGroupSnapshotResponseLun]:
    """Transform luns into OntapConsistencyGroupSnapshotResponseLun list."""
    return [OntapConsistencyGroupSnapshotResponseLun(**item) for item in record.get("luns", [])]


def _transform_missing_luns(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupSnapshotResponseMissingLun]:
    """Transform missing_luns into OntapConsistencyGroupSnapshotResponseMissingLun list."""
    return [
        OntapConsistencyGroupSnapshotResponseMissingLun(**item)
        for item in record.get("missing_luns", [])
    ]


def _transform_missing_namespaces(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupSnapshotResponseMissingNamespace]:
    """Transform missing_namespaces into OntapConsistencyGroupSnapshotResponseMissingNamespace list."""
    return [
        OntapConsistencyGroupSnapshotResponseMissingNamespace(**item)
        for item in record.get("missing_namespaces", [])
    ]


def _transform_missing_volumes(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupSnapshotResponseMissingVolume]:
    """Transform missing_volumes into OntapConsistencyGroupSnapshotResponseMissingVolume list."""
    return [
        OntapConsistencyGroupSnapshotResponseMissingVolume(**item)
        for item in record.get("missing_volumes", [])
    ]


def _transform_namespaces(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupSnapshotResponseNamespace]:
    """Transform namespaces into OntapConsistencyGroupSnapshotResponseNamespace list."""
    return [
        OntapConsistencyGroupSnapshotResponseNamespace(**item)
        for item in record.get("namespaces", [])
    ]


def _transform_snapshot_volumes(
    record: dict[str, Any],
) -> list[OntapConsistencyGroupSnapshotResponseSnapshotVolume]:
    """Transform snapshot_volumes into OntapConsistencyGroupSnapshotResponseSnapshotVolume list."""
    return [
        OntapConsistencyGroupSnapshotResponseSnapshotVolume(**item)
        for item in record.get("snapshot_volumes", [])
    ]


ONTAPCONSISTENCYGROUPSNAPSHOTRESPONSE_MAPPING = TypeMapping(
    name="OntapConsistencyGroupSnapshotResponse",
    model_class=OntapConsistencyGroupSnapshotResponse,
    api_endpoint="/application/consistency-groups/{consistency_group.uuid}/snapshots?fields=*",
    api_type="ontap",
    parent_mapping="OntapConsistencyGroupResponse",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="consistency_group_name",
            api_path="consistency_group.name",
        ),
        FieldMapping(
            cache_attr="consistency_group_uuid",
            api_path="consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="consistency_type",
            api_path="consistency_type",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="is_partial",
            api_path="is_partial",
            default=False,
        ),
        FieldMapping(
            cache_attr="luns",
            api_path="luns",
            transform=_transform_luns,
            default=[],
        ),
        FieldMapping(
            cache_attr="missing_luns",
            api_path="missing_luns",
            transform=_transform_missing_luns,
            default=[],
        ),
        FieldMapping(
            cache_attr="missing_namespaces",
            api_path="missing_namespaces",
            transform=_transform_missing_namespaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="missing_volumes",
            api_path="missing_volumes",
            transform=_transform_missing_volumes,
            default=[],
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
            cache_attr="reclaimable_space",
            api_path="reclaimable_space",
            default=0,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="restore_size",
            api_path="restore_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="snapmirror_label",
            api_path="snapmirror_label",
        ),
        FieldMapping(
            cache_attr="snapshot_volumes",
            api_path="snapshot_volumes",
            transform=_transform_snapshot_volumes,
            default=[],
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
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="write_fence",
            api_path="write_fence",
            default=False,
        ),
    ),
)

model_registry.register_mapping(
    "OntapConsistencyGroupSnapshotResponse", ONTAPCONSISTENCYGROUPSNAPSHOTRESPONSE_MAPPING
)
