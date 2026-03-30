"""OntapConsistencyGroupSnapshotResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupSnapshotResponseLun(OntapModel):
    """OntapConsistencyGroupSnapshotResponseLun sub-model for luns."""

    luns_name: str = ""
    luns_uuid: str = ""


class OntapConsistencyGroupSnapshotResponseMissingLun(OntapModel):
    """OntapConsistencyGroupSnapshotResponseMissingLun sub-model for missing_luns."""

    missing_luns_name: str = ""
    missing_luns_uuid: str = ""


class OntapConsistencyGroupSnapshotResponseMissingNamespace(OntapModel):
    """OntapConsistencyGroupSnapshotResponseMissingNamespace sub-model for missing_namespaces."""

    missing_namespaces_name: str = ""
    missing_namespaces_uuid: str = ""


class OntapConsistencyGroupSnapshotResponseMissingVolume(OntapModel):
    """OntapConsistencyGroupSnapshotResponseMissingVolume sub-model for missing_volumes."""

    missing_volumes_name: str = ""
    missing_volumes_uuid: str = ""


class OntapConsistencyGroupSnapshotResponseNamespace(OntapModel):
    """OntapConsistencyGroupSnapshotResponseNamespace sub-model for namespaces."""

    namespaces_name: str = ""
    namespaces_uuid: str = ""


class OntapConsistencyGroupSnapshotResponseSnapshotVolume(OntapModel):
    """OntapConsistencyGroupSnapshotResponseSnapshotVolume sub-model for snapshot_volumes."""

    snapshot_volumes_snapshot_name: str = ""
    snapshot_volumes_snapshot_uuid: str = ""
    snapshot_volumes_volume_name: str = ""
    snapshot_volumes_volume_uuid: str = ""


class OntapConsistencyGroupSnapshotResponse(OntapModel):
    """OntapConsistencyGroupSnapshotResponse information."""

    comment: str = ""
    consistency_group_name: str = ""
    consistency_group_uuid: str = ""
    consistency_type: str = ""
    create_time: str = ""
    is_partial: bool = False
    luns: list[OntapConsistencyGroupSnapshotResponseLun] = Field(default_factory=list)
    missing_luns: list[OntapConsistencyGroupSnapshotResponseMissingLun] = Field(
        default_factory=list
    )
    missing_namespaces: list[OntapConsistencyGroupSnapshotResponseMissingNamespace] = Field(
        default_factory=list
    )
    missing_volumes: list[OntapConsistencyGroupSnapshotResponseMissingVolume] = Field(
        default_factory=list
    )
    name: str = ""
    namespaces: list[OntapConsistencyGroupSnapshotResponseNamespace] = Field(default_factory=list)
    reclaimable_space: int = 0
    restore_size: int = 0
    snapmirror_label: str = ""
    snapshot_volumes: list[OntapConsistencyGroupSnapshotResponseSnapshotVolume] = Field(
        default_factory=list
    )
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    write_fence: bool = False
