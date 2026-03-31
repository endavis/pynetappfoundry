"""OntapConsistencyGroupSnapshotResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupSnapshotResponseLun(OntapModel):
    """OntapConsistencyGroupSnapshotResponseLun sub-model for luns."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupSnapshotResponseMissingLun(OntapModel):
    """OntapConsistencyGroupSnapshotResponseMissingLun sub-model for missing_luns."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupSnapshotResponseMissingNamespace(OntapModel):
    """OntapConsistencyGroupSnapshotResponseMissingNamespace sub-model for missing_namespaces."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupSnapshotResponseMissingVolume(OntapModel):
    """OntapConsistencyGroupSnapshotResponseMissingVolume sub-model for missing_volumes."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupSnapshotResponseNamespace(OntapModel):
    """OntapConsistencyGroupSnapshotResponseNamespace sub-model for namespaces."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupSnapshotResponseSnapshotVolume(OntapModel):
    """OntapConsistencyGroupSnapshotResponseSnapshotVolume sub-model for snapshot_volumes."""

    snapshot_name: str = ""
    snapshot_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


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
