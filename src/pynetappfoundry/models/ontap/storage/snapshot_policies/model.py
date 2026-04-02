"""OntapSnapshotPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnapshotPolicyCopySchedule(OntapModel):
    """OntapSnapshotPolicyCopySchedule sub-model for schedule."""

    name: str = ""
    uuid: str = ""


class OntapSnapshotPolicyCopy(OntapModel):
    """OntapSnapshotPolicyCopy sub-model for copies."""

    count: int = 0
    prefix: str = ""
    retention_period: str = ""
    schedule: OntapSnapshotPolicyCopySchedule = Field(
        default_factory=OntapSnapshotPolicyCopySchedule
    )
    snapmirror_label: str = ""


class OntapSnapshotPolicySvm(OntapModel):
    """OntapSnapshotPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnapshotPolicy(OntapModel):
    """OntapSnapshotPolicy information."""

    comment: str = ""
    copies: list[OntapSnapshotPolicyCopy] = Field(default_factory=list)
    enabled: bool = False
    name: str = ""
    scope: str = ""
    svm: OntapSnapshotPolicySvm = Field(default_factory=OntapSnapshotPolicySvm)
    uuid: str = ""
