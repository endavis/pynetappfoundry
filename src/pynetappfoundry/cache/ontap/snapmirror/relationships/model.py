# ruff: noqa: E501
"""OntapSnapmirrorRelationship information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapSnapmirrorRelationshipArgument(CacheModel):
    """OntapSnapmirrorRelationshipArgument sub-model for arguments."""

    consistency_group_failover_error_arguments_code: str = ""
    consistency_group_failover_error_arguments_message: str = ""


class OntapSnapmirrorRelationshipConsistencyGroupVolume(CacheModel):
    """OntapSnapmirrorRelationshipConsistencyGroupVolume sub-model for consistency_group_volumes."""

    destination_consistency_group_volumes_name: str = ""
    destination_consistency_group_volumes_uuid: str = ""


class OntapSnapmirrorRelationshipConsistencyGroupVolume2(CacheModel):
    """OntapSnapmirrorRelationshipConsistencyGroupVolume2 sub-model for consistency_group_volumes."""

    source_consistency_group_volumes_name: str = ""
    source_consistency_group_volumes_uuid: str = ""


class OntapSnapmirrorRelationshipSvmdrVolume(CacheModel):
    """OntapSnapmirrorRelationshipSvmdrVolume sub-model for svmdr_volumes."""

    svmdr_volumes_name: str = ""


class OntapSnapmirrorRelationshipUnhealthyReason(CacheModel):
    """OntapSnapmirrorRelationshipUnhealthyReason sub-model for unhealthy_reason."""

    unhealthy_reason_arguments: list[str] = Field(default_factory=list)
    unhealthy_reason_code: str = ""
    unhealthy_reason_message: str = ""


class OntapSnapmirrorRelationship(CacheModel):
    """OntapSnapmirrorRelationship information."""

    backoff_level: str = ""
    consistency_group_failover_error_arguments: list[OntapSnapmirrorRelationshipArgument] = Field(
        default_factory=list
    )
    consistency_group_failover_error_code: str = ""
    consistency_group_failover_error_message: str = ""
    consistency_group_failover_state: str = ""
    consistency_group_failover_status_code: str = ""
    consistency_group_failover_status_message: str = ""
    consistency_group_failover_type: str = ""
    create_destination_bucket_retention_default_period: str = ""
    create_destination_bucket_retention_mode: str = ""
    create_destination_enabled: bool = False
    create_destination_size: int = 0
    create_destination_snapshot_locking_enabled: bool = False
    create_destination_storage_service_enabled: bool = False
    create_destination_storage_service_enforce_performance: bool = False
    create_destination_storage_service_name: str = ""
    create_destination_tiering_policy: str = ""
    create_destination_tiering_supported: bool = False
    destination_cluster_name: str = ""
    destination_cluster_uuid: OntapUUID = ""
    destination_consistency_group_volumes: list[
        OntapSnapmirrorRelationshipConsistencyGroupVolume
    ] = Field(default_factory=list)
    destination_ipspace: str = ""
    destination_luns_name: str = ""
    destination_luns_uuid: str = ""
    destination_path: str = ""
    destination_svm_name: str = ""
    destination_svm_uuid: str = ""
    exported_snapshot: str = ""
    group_type: str = ""
    healthy: bool = False
    identity_preservation: str = ""
    io_serving_copy: str = ""
    lag_time: str = ""
    last_transfer_network_compression_ratio: str = ""
    last_transfer_type: str = ""
    master_bias_activated_site: str = ""
    policy_name: str = ""
    policy_type: str = ""
    policy_uuid: OntapUUID = ""
    preferred_site: str = ""
    preserve: bool = False
    quick_resync: bool = False
    recover_after_break: bool = False
    restore: bool = False
    restore_to_snapshot: str = ""
    source_cluster_name: str = ""
    source_cluster_uuid: OntapUUID = ""
    source_consistency_group_volumes: list[OntapSnapmirrorRelationshipConsistencyGroupVolume2] = (
        Field(default_factory=list)
    )
    source_luns_name: str = ""
    source_luns_uuid: str = ""
    source_path: str = ""
    source_svm_name: str = ""
    source_svm_uuid: str = ""
    state: str = ""
    svmdr_volumes: list[OntapSnapmirrorRelationshipSvmdrVolume] = Field(default_factory=list)
    throttle: int = 0
    total_transfer_bytes: int = 0
    total_transfer_duration: str = ""
    transfer_bytes_transferred: int = 0
    transfer_end_time: str = ""
    transfer_last_updated_time: str = ""
    transfer_state: str = ""
    transfer_total_duration: str = ""
    transfer_type: str = ""
    transfer_uuid: OntapUUID = ""
    transfer_schedule_name: str = ""
    transfer_schedule_uuid: str = ""
    unhealthy_reason: list[OntapSnapmirrorRelationshipUnhealthyReason] = Field(default_factory=list)
    uuid: OntapUUID = ""
