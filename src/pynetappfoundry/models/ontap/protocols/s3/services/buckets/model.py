"""OntapS3BucketSvm information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3BucketSvmAggregate(OntapModel):
    """OntapS3BucketSvmAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketSvmRule(OntapModel):
    """OntapS3BucketSvmRule sub-model for rules."""

    allowed_headers: list[str] = Field(default_factory=list)
    allowed_methods: list[str] = Field(default_factory=list)
    allowed_origins: list[str] = Field(default_factory=list)
    expose_headers: list[str] = Field(default_factory=list)
    id: str = ""
    max_age_seconds: int = 0


class OntapS3BucketSvmRule2(OntapModel):
    """OntapS3BucketSvmRule2 sub-model for rules."""

    abort_incomplete_multipart_upload_after_initiation_days: int = 0
    bucket_name: str = ""
    enabled: bool = False
    expiration_expired_object_delete_marker: bool = False
    expiration_object_age_days: int = 0
    expiration_object_expiry_date: str = ""
    name: str = ""
    non_current_version_expiration_new_non_current_versions: int = 0
    non_current_version_expiration_non_current_days: int = 0
    object_filter_prefix: str = ""
    object_filter_size_greater_than: int = 0
    object_filter_size_less_than: int = 0
    object_filter_tags: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: OntapUUID = ""


class OntapS3BucketSvmStatement(OntapModel):
    """OntapS3BucketSvmStatement sub-model for statements."""

    actions: list[str] = Field(default_factory=list)
    conditions: list[dict[str, Any]] = Field(default_factory=list)
    effect: str = ""
    principals: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapS3BucketSvm(OntapModel):
    """OntapS3BucketSvm information."""

    aggregates: list[OntapS3BucketSvmAggregate] = Field(default_factory=list)
    audit_event_selector_access: str = ""
    audit_event_selector_permission: str = ""
    comment: str = ""
    constituents_per_aggregate: int = 0
    cors_rules: list[OntapS3BucketSvmRule] = Field(default_factory=list)
    encryption_enabled: bool = False
    lifecycle_management_rules: list[OntapS3BucketSvmRule2] = Field(default_factory=list)
    logical_used_size: int = 0
    name: str = ""
    nas_path: str = ""
    policy_statements: list[OntapS3BucketSvmStatement] = Field(default_factory=list)
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
    type_: str = ""
    uuid: OntapUUID = ""
    versioning_state: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
