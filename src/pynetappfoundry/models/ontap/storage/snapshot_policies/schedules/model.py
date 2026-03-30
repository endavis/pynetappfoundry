"""OntapSnapshotPolicySchedule information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSnapshotPolicySchedule(OntapModel):
    """OntapSnapshotPolicySchedule information."""

    count: int = 0
    prefix: str = ""
    retention_period: str = ""
    schedule_name: str = ""
    schedule_uuid: str = ""
    snapmirror_label: str = ""
    snapshot_policy_name: str = ""
    snapshot_policy_uuid: str = ""
