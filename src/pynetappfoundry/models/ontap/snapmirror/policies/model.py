# ruff: noqa: E501
"""OntapSnapmirrorPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSnapmirrorPolicyRetentionCreationSchedule(OntapModel):
    """OntapSnapmirrorPolicyRetentionCreationSchedule sub-model for creation_schedule."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorPolicyRetention(OntapModel):
    """OntapSnapmirrorPolicyRetention sub-model for retention."""

    count: int = 0
    creation_schedule: OntapSnapmirrorPolicyRetentionCreationSchedule = Field(
        default_factory=OntapSnapmirrorPolicyRetentionCreationSchedule
    )
    label: str = ""
    period: str = ""
    prefix: str = ""
    preserve: bool = False
    warn: int = 0


class OntapSnapmirrorPolicySvm(OntapModel):
    """OntapSnapmirrorPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorPolicySyncCommonSnapshotSchedule(OntapModel):
    """OntapSnapmirrorPolicySyncCommonSnapshotSchedule sub-model for sync_common_snapshot_schedule."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorPolicyTransferSchedule(OntapModel):
    """OntapSnapmirrorPolicyTransferSchedule sub-model for transfer_schedule."""

    name: str = ""
    uuid: str = ""


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
    svm: OntapSnapmirrorPolicySvm = Field(default_factory=OntapSnapmirrorPolicySvm)
    sync_common_snapshot_schedule: OntapSnapmirrorPolicySyncCommonSnapshotSchedule = Field(
        default_factory=OntapSnapmirrorPolicySyncCommonSnapshotSchedule
    )
    sync_type: str = ""
    throttle: int = 0
    transfer_schedule: OntapSnapmirrorPolicyTransferSchedule = Field(
        default_factory=OntapSnapmirrorPolicyTransferSchedule
    )
    type_: str = ""
    uuid: OntapUUID = ""
