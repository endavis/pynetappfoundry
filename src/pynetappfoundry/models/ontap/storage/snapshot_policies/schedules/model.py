"""OntapSnapshotPolicySchedule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnapshotPolicyScheduleSchedule(OntapModel):
    """OntapSnapshotPolicyScheduleSchedule sub-model for schedule."""

    name: str = ""
    uuid: str = ""


class OntapSnapshotPolicyScheduleSnapshotPolicy(OntapModel):
    """OntapSnapshotPolicyScheduleSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapSnapshotPolicySchedule(OntapModel):
    """OntapSnapshotPolicySchedule information."""

    count: int = 0
    prefix: str = ""
    retention_period: str = ""
    schedule: OntapSnapshotPolicyScheduleSchedule = Field(
        default_factory=OntapSnapshotPolicyScheduleSchedule
    )
    snapmirror_label: str = ""
    snapshot_policy: OntapSnapshotPolicyScheduleSnapshotPolicy = Field(
        default_factory=OntapSnapshotPolicyScheduleSnapshotPolicy
    )
