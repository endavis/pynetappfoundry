"""OntapSnapmirrorPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSnapmirrorPolicyRetention(OntapModel):
    """OntapSnapmirrorPolicyRetention sub-model for retention."""

    count: int = 0
    creation_schedule_name: str = ""
    creation_schedule_uuid: str = ""
    label: str = ""
    period: str = ""
    prefix: str = ""
    preserve: bool = False
    warn: int = 0


class OntapSnapmirrorPolicy(OntapModel):
    """OntapSnapmirrorPolicy information."""

    comment: str = ""
    copy_all_source_snapshots: bool = False
    copy_latest_source_snapshot: bool = False
    create_snapshot_on_source: bool = False
    identity_preservation: str = ""
    name: str = ""
    network_compression_enabled: bool = False
    retention: list[OntapSnapmirrorPolicyRetention] = Field(default_factory=list)
    rpo: int = 0
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    sync_common_snapshot_schedule_name: str = ""
    sync_common_snapshot_schedule_uuid: str = ""
    sync_type: str = ""
    throttle: int = 0
    transfer_schedule_name: str = ""
    transfer_schedule_uuid: str = ""
    type_: str = ""
    uuid: OntapUUID = ""
