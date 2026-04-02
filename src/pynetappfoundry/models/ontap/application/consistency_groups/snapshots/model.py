"""OntapConsistencyGroupSnapshotResponse information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupSnapshotResponseConsistencyGroup(OntapModel):
    """OntapConsistencyGroupSnapshotResponseConsistencyGroup sub-model for consistency_group."""

    name: str = ""
    uuid: str = ""


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


class OntapConsistencyGroupSnapshotResponseSvm(OntapModel):
    """OntapConsistencyGroupSnapshotResponseSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupSnapshotResponse(OntapModel):
    """OntapConsistencyGroupSnapshotResponse information."""

    comment: str = ""
    consistency_group: OntapConsistencyGroupSnapshotResponseConsistencyGroup = Field(
        default_factory=OntapConsistencyGroupSnapshotResponseConsistencyGroup
    )
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
    snapshot_volumes: list[dict[str, Any]] = Field(default_factory=list)
    svm: OntapConsistencyGroupSnapshotResponseSvm = Field(
        default_factory=OntapConsistencyGroupSnapshotResponseSvm
    )
    uuid: str = ""
    write_fence: bool = False
