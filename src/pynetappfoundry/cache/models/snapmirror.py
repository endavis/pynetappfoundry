"""SnapMirror relationship models (/snapmirror API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class SnapMirrorRelationship(BaseModel):
    """SnapMirror relationship information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    source_path: str = ""
    destination_path: str = ""
    relationship_type: str = ""  # async, sync, etc.
    policy_uuid: str = ""
    throttle: int = 0  # KB/s, 0 = unlimited
    group_type: str = ""  # none, svm_dr, consistency_group
    transfer_schedule_uuid: str = ""
