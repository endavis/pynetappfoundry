"""OntapSnapshotPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnapshotPolicyCopy(OntapModel):
    """OntapSnapshotPolicyCopy sub-model for copies."""

    count: int = 0
    prefix: str = ""
    retention_period: str = ""
    schedule_name: str = ""
    schedule_uuid: str = ""
    snapmirror_label: str = ""


class OntapSnapshotPolicy(OntapModel):
    """OntapSnapshotPolicy information."""

    comment: str = ""
    copies: list[OntapSnapshotPolicyCopy] = Field(default_factory=list)
    enabled: bool = False
    name: str = ""
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
