"""OntapS3Service information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3ServiceBucket(OntapModel):
    """OntapS3ServiceBucket sub-model for buckets."""

    buckets_aggregates: list[dict[str, Any]] = Field(default_factory=list)
    buckets_allowed: bool = False
    buckets_audit_event_selector_access: str = ""
    buckets_audit_event_selector_permission: str = ""
    buckets_comment: str = ""
    buckets_constituents_per_aggregate: int = 0
    buckets_cors_rules: list[dict[str, Any]] = Field(default_factory=list)
    buckets_encryption_enabled: bool = False
    buckets_lifecycle_management_rules: list[dict[str, Any]] = Field(default_factory=list)
    buckets_logical_used_size: int = 0
    buckets_name: str = ""
    buckets_nas_path: str = ""
    buckets_policy_statements: list[dict[str, Any]] = Field(default_factory=list)
    buckets_protection_status_destination_is_cloud: bool = False
    buckets_protection_status_destination_is_external_cloud: bool = False
    buckets_protection_status_destination_is_ontap: bool = False
    buckets_protection_status_is_protected: bool = False
    buckets_qos_policy_max_throughput_iops: int = 0
    buckets_qos_policy_max_throughput_mbps: int = 0
    buckets_qos_policy_min_throughput_iops: int = 0
    buckets_qos_policy_min_throughput_mbps: int = 0
    buckets_qos_policy_name: str = ""
    buckets_qos_policy_uuid: str = ""
    buckets_retention_default_period: str = ""
    buckets_retention_mode: str = ""
    buckets_role: str = ""
    buckets_size: int = 0
    buckets_snapshot_policy_name: str = ""
    buckets_snapshot_policy_uuid: OntapUUID = ""
    buckets_storage_service_level: str = ""
    buckets_svm_name: str = ""
    buckets_svm_uuid: str = ""
    buckets_type: str = ""
    buckets_use_mirrored_aggregates: bool = False
    buckets_uuid: OntapUUID = ""
    buckets_versioning_state: str = ""
    buckets_volume_name: str = ""
    buckets_volume_uuid: str = ""


class OntapS3ServiceUser(OntapModel):
    """OntapS3ServiceUser sub-model for users."""

    users_access_key: str = ""
    users_comment: str = ""
    users_key_expiry_time: str = ""
    users_key_time_to_live: str = ""
    users_name: str = ""
    users_secret_key: str = ""
    users_svm_name: str = ""
    users_svm_uuid: str = ""


class OntapS3Service(OntapModel):
    """OntapS3Service information."""

    buckets: list[OntapS3ServiceBucket] = Field(default_factory=list)
    certificate_name: str = ""
    certificate_uuid: str = ""
    comment: str = ""
    default_unix_user: str = ""
    default_win_user: str = ""
    enabled: bool = False
    is_http_enabled: bool = False
    is_https_enabled: bool = False
    max_key_time_to_live: str = ""
    max_lock_retention_period: str = ""
    metric_duration: str = ""
    metric_iops_other: int = 0
    metric_iops_read: int = 0
    metric_iops_total: int = 0
    metric_iops_write: int = 0
    metric_latency_other: int = 0
    metric_latency_read: int = 0
    metric_latency_total: int = 0
    metric_latency_write: int = 0
    metric_status: str = ""
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    min_lock_retention_period: str = ""
    name: str = ""
    port: int = 0
    secure_port: int = 0
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    users: list[OntapS3ServiceUser] = Field(default_factory=list)
