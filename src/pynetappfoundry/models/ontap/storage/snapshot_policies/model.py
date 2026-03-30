"""OntapSnapshotPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnapshotPolicyCopy(OntapModel):
    """OntapSnapshotPolicyCopy sub-model for copies."""

    copies_count: int = 0
    copies_prefix: str = ""
    copies_retention_period: str = ""
    copies_schedule_name: str = ""
    copies_schedule_uuid: str = ""
    copies_snapmirror_label: str = ""


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
