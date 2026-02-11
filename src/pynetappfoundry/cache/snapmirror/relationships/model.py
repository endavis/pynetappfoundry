"""SnapMirror relationship information — /snapmirror/relationships."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class SnapMirrorRelationship(CacheModel):
    """SnapMirror relationship information."""

    uuid: str = ""
    source_path: str = ""
    destination_path: str = ""
    relationship_type: str = ""  # async, sync, etc.
    policy_uuid: str = ""
    throttle: int = 0  # KB/s, 0 = unlimited
    group_type: str = ""  # none, svm_dr, consistency_group
    transfer_schedule_uuid: str = ""
