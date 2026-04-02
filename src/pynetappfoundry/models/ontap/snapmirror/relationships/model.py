# ruff: noqa: E501
"""OntapSnapmirrorRelationship information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument(OntapModel):
    """OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapSnapmirrorRelationshipConsistencyGroupFailoverError(OntapModel):
    """OntapSnapmirrorRelationshipConsistencyGroupFailoverError sub-model for error."""

    arguments: list[OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument] = Field(
        default_factory=list
    )
    code: str = ""
    message: str = ""


class OntapSnapmirrorRelationshipConsistencyGroupFailoverStatus(OntapModel):
    """OntapSnapmirrorRelationshipConsistencyGroupFailoverStatus sub-model for status."""

    code: str = ""
    message: str = ""


class OntapSnapmirrorRelationshipConsistencyGroupFailover(OntapModel):
    """OntapSnapmirrorRelationshipConsistencyGroupFailover sub-model for consistency_group_failover."""

    error: OntapSnapmirrorRelationshipConsistencyGroupFailoverError = Field(
        default_factory=OntapSnapmirrorRelationshipConsistencyGroupFailoverError
    )
    state: str = ""
    status: OntapSnapmirrorRelationshipConsistencyGroupFailoverStatus = Field(
        default_factory=OntapSnapmirrorRelationshipConsistencyGroupFailoverStatus
    )
    type_: str = ""


class OntapSnapmirrorRelationshipCreateDestinationBucketRetention(OntapModel):
    """OntapSnapmirrorRelationshipCreateDestinationBucketRetention sub-model for bucket_retention."""

    default_period: str = ""
    mode: str = ""


class OntapSnapmirrorRelationshipCreateDestinationStorageService(OntapModel):
    """OntapSnapmirrorRelationshipCreateDestinationStorageService sub-model for storage_service."""

    enabled: bool = False
    enforce_performance: bool = False
    name: str = ""


class OntapSnapmirrorRelationshipCreateDestinationTiering(OntapModel):
    """OntapSnapmirrorRelationshipCreateDestinationTiering sub-model for tiering."""

    policy: str = ""
    supported: bool = False


class OntapSnapmirrorRelationshipCreateDestination(OntapModel):
    """OntapSnapmirrorRelationshipCreateDestination sub-model for create_destination."""

    bucket_retention: OntapSnapmirrorRelationshipCreateDestinationBucketRetention = Field(
        default_factory=OntapSnapmirrorRelationshipCreateDestinationBucketRetention
    )
    enabled: bool = False
    size: int = 0
    snapshot_locking_enabled: bool = False
    storage_service: OntapSnapmirrorRelationshipCreateDestinationStorageService = Field(
        default_factory=OntapSnapmirrorRelationshipCreateDestinationStorageService
    )
    tiering: OntapSnapmirrorRelationshipCreateDestinationTiering = Field(
        default_factory=OntapSnapmirrorRelationshipCreateDestinationTiering
    )


class OntapSnapmirrorRelationshipDestinationCluster(OntapModel):
    """OntapSnapmirrorRelationshipDestinationCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume(OntapModel):
    """OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume sub-model for consistency_group_volumes."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipDestinationLuns(OntapModel):
    """OntapSnapmirrorRelationshipDestinationLuns sub-model for luns."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipDestinationSvm(OntapModel):
    """OntapSnapmirrorRelationshipDestinationSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipDestination(OntapModel):
    """OntapSnapmirrorRelationshipDestination sub-model for destination."""

    cluster: OntapSnapmirrorRelationshipDestinationCluster = Field(
        default_factory=OntapSnapmirrorRelationshipDestinationCluster
    )
    consistency_group_volumes: list[
        OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume
    ] = Field(default_factory=list)
    ipspace: str = ""
    luns: OntapSnapmirrorRelationshipDestinationLuns = Field(
        default_factory=OntapSnapmirrorRelationshipDestinationLuns
    )
    path: str = ""
    svm: OntapSnapmirrorRelationshipDestinationSvm = Field(
        default_factory=OntapSnapmirrorRelationshipDestinationSvm
    )


class OntapSnapmirrorRelationshipPolicy(OntapModel):
    """OntapSnapmirrorRelationshipPolicy sub-model for policy."""

    name: str = ""
    type_: str = ""
    uuid: OntapUUID = ""


class OntapSnapmirrorRelationshipSourceCluster(OntapModel):
    """OntapSnapmirrorRelationshipSourceCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapSnapmirrorRelationshipSourceConsistencyGroupVolume(OntapModel):
    """OntapSnapmirrorRelationshipSourceConsistencyGroupVolume sub-model for consistency_group_volumes."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipSourceLuns(OntapModel):
    """OntapSnapmirrorRelationshipSourceLuns sub-model for luns."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipSourceSvm(OntapModel):
    """OntapSnapmirrorRelationshipSourceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipSource(OntapModel):
    """OntapSnapmirrorRelationshipSource sub-model for source."""

    cluster: OntapSnapmirrorRelationshipSourceCluster = Field(
        default_factory=OntapSnapmirrorRelationshipSourceCluster
    )
    consistency_group_volumes: list[OntapSnapmirrorRelationshipSourceConsistencyGroupVolume] = (
        Field(default_factory=list)
    )
    luns: OntapSnapmirrorRelationshipSourceLuns = Field(
        default_factory=OntapSnapmirrorRelationshipSourceLuns
    )
    path: str = ""
    svm: OntapSnapmirrorRelationshipSourceSvm = Field(
        default_factory=OntapSnapmirrorRelationshipSourceSvm
    )


class OntapSnapmirrorRelationshipSvmdrVolume(OntapModel):
    """OntapSnapmirrorRelationshipSvmdrVolume sub-model for svmdr_volumes."""

    name: str = ""


class OntapSnapmirrorRelationshipTransfer(OntapModel):
    """OntapSnapmirrorRelationshipTransfer sub-model for transfer."""

    bytes_transferred: int = 0
    end_time: str = ""
    last_updated_time: str = ""
    state: str = ""
    total_duration: str = ""
    type_: str = ""
    uuid: OntapUUID = ""


class OntapSnapmirrorRelationshipTransferSchedule(OntapModel):
    """OntapSnapmirrorRelationshipTransferSchedule sub-model for transfer_schedule."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorRelationshipUnhealthyReason(OntapModel):
    """OntapSnapmirrorRelationshipUnhealthyReason sub-model for unhealthy_reason."""

    arguments: list[str] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapSnapmirrorRelationship(OntapModel):
    """OntapSnapmirrorRelationship information."""

    backoff_level: str = ""
    consistency_group_failover: OntapSnapmirrorRelationshipConsistencyGroupFailover = Field(
        default_factory=OntapSnapmirrorRelationshipConsistencyGroupFailover
    )
    create_destination: OntapSnapmirrorRelationshipCreateDestination = Field(
        default_factory=OntapSnapmirrorRelationshipCreateDestination
    )
    destination: OntapSnapmirrorRelationshipDestination = Field(
        default_factory=OntapSnapmirrorRelationshipDestination
    )
    exported_snapshot: str = ""
    group_type: str = ""
    healthy: bool = False
    identity_preservation: str = ""
    io_serving_copy: str = ""
    lag_time: str = ""
    last_transfer_network_compression_ratio: str = ""
    last_transfer_type: str = ""
    master_bias_activated_site: str = ""
    policy: OntapSnapmirrorRelationshipPolicy = Field(
        default_factory=OntapSnapmirrorRelationshipPolicy
    )
    preferred_site: str = ""
    preserve: bool = False
    quick_resync: bool = False
    recover_after_break: bool = False
    restore: bool = False
    restore_to_snapshot: str = ""
    source: OntapSnapmirrorRelationshipSource = Field(
        default_factory=OntapSnapmirrorRelationshipSource
    )
    state: str = ""
    svmdr_volumes: list[OntapSnapmirrorRelationshipSvmdrVolume] = Field(default_factory=list)
    throttle: int = 0
    total_transfer_bytes: int = 0
    total_transfer_duration: str = ""
    transfer: OntapSnapmirrorRelationshipTransfer = Field(
        default_factory=OntapSnapmirrorRelationshipTransfer
    )
    transfer_schedule: OntapSnapmirrorRelationshipTransferSchedule = Field(
        default_factory=OntapSnapmirrorRelationshipTransferSchedule
    )
    unhealthy_reason: list[OntapSnapmirrorRelationshipUnhealthyReason] = Field(default_factory=list)
    uuid: OntapUUID = ""
