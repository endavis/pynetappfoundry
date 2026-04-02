"""OntapSnapshot information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnapshotDelta(OntapModel):
    """OntapSnapshotDelta sub-model for delta."""

    size_consumed: int = 0
    time_elapsed: str = ""


class OntapSnapshotProvenanceVolume(OntapModel):
    """OntapSnapshotProvenanceVolume sub-model for provenance_volume."""

    uuid: str = ""


class OntapSnapshotSnaplock(OntapModel):
    """OntapSnapshotSnaplock sub-model for snaplock."""

    expired: bool = False
    expiry_time: str = ""
    time_until_expiry: str = ""


class OntapSnapshotSvm(OntapModel):
    """OntapSnapshotSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnapshotVolume(OntapModel):
    """OntapSnapshotVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapSnapshot(OntapModel):
    """OntapSnapshot information."""

    comment: str = ""
    compress_savings: int = 0
    create_time: str = ""
    dedup_savings: int = 0
    delta: OntapSnapshotDelta = Field(default_factory=OntapSnapshotDelta)
    expiry_time: str = ""
    logical_size: int = 0
    name: str = ""
    owners: list[str] = Field(default_factory=list)
    provenance_volume: OntapSnapshotProvenanceVolume = Field(
        default_factory=OntapSnapshotProvenanceVolume
    )
    reclaimable_space: int = 0
    size: int = 0
    snaplock: OntapSnapshotSnaplock = Field(default_factory=OntapSnapshotSnaplock)
    snaplock_expiry_time: str = ""
    snapmirror_label: str = ""
    state: str = ""
    svm: OntapSnapshotSvm = Field(default_factory=OntapSnapshotSvm)
    uuid: str = ""
    vbn0_savings: int = 0
    version_uuid: str = ""
    volume: OntapSnapshotVolume = Field(default_factory=OntapSnapshotVolume)
