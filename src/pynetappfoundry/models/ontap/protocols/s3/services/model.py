"""OntapS3Service information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3ServiceBucket(OntapModel):
    """OntapS3ServiceBucket sub-model for buckets."""

    aggregates: list[dict[str, Any]] = Field(default_factory=list)
    allowed: bool = False
    audit_event_selector_access: str = ""
    audit_event_selector_permission: str = ""
    comment: str = ""
    constituents_per_aggregate: int = 0
    cors_rules: list[dict[str, Any]] = Field(default_factory=list)
    encryption_enabled: bool = False
    lifecycle_management_rules: list[dict[str, Any]] = Field(default_factory=list)
    logical_used_size: int = 0
    name: str = ""
    nas_path: str = ""
    policy_statements: list[dict[str, Any]] = Field(default_factory=list)
    protection_status_destination_is_cloud: bool = False
    protection_status_destination_is_external_cloud: bool = False
    protection_status_destination_is_ontap: bool = False
    protection_status_is_protected: bool = False
    qos_policy_max_throughput_iops: int = 0
    qos_policy_max_throughput_mbps: int = 0
    qos_policy_min_throughput_iops: int = 0
    qos_policy_min_throughput_mbps: int = 0
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    retention_default_period: str = ""
    retention_mode: str = ""
    role: str = ""
    size: int = 0
    snapshot_policy_name: str = ""
    snapshot_policy_uuid: OntapUUID = ""
    storage_service_level: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type: str = ""
    use_mirrored_aggregates: bool = False
    uuid: OntapUUID = ""
    versioning_state: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


class OntapS3ServiceUser(OntapModel):
    """OntapS3ServiceUser sub-model for users."""

    access_key: str = ""
    comment: str = ""
    key_expiry_time: str = ""
    key_time_to_live: str = ""
    name: str = ""
    secret_key: str = ""
    svm_name: str = ""
    svm_uuid: str = ""


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
