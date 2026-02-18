"""OntapS3BucketSvm information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapS3BucketSvmAggregate(CacheModel):
    """OntapS3BucketSvmAggregate sub-model for aggregates."""

    aggregates_name: str = ""
    aggregates_uuid: str = ""


class OntapS3BucketSvmRule(CacheModel):
    """OntapS3BucketSvmRule sub-model for rules."""

    cors_rules_allowed_headers: list[str] = Field(default_factory=list)
    cors_rules_allowed_methods: list[str] = Field(default_factory=list)
    cors_rules_allowed_origins: list[str] = Field(default_factory=list)
    cors_rules_expose_headers: list[str] = Field(default_factory=list)
    cors_rules_id: str = ""
    cors_rules_max_age_seconds: int = 0


class OntapS3BucketSvmRule2(CacheModel):
    """OntapS3BucketSvmRule2 sub-model for rules."""

    lifecycle_management_rules_abort_incomplete_multipart_upload_after_initiation_days: int = 0
    lifecycle_management_rules_bucket_name: str = ""
    lifecycle_management_rules_enabled: bool = False
    lifecycle_management_rules_expiration_expired_object_delete_marker: bool = False
    lifecycle_management_rules_expiration_object_age_days: int = 0
    lifecycle_management_rules_expiration_object_expiry_date: str = ""
    lifecycle_management_rules_name: str = ""
    lifecycle_management_rules_non_current_version_expiration_new_non_current_versions: int = 0
    lifecycle_management_rules_non_current_version_expiration_non_current_days: int = 0
    lifecycle_management_rules_object_filter_prefix: str = ""
    lifecycle_management_rules_object_filter_size_greater_than: int = 0
    lifecycle_management_rules_object_filter_size_less_than: int = 0
    lifecycle_management_rules_object_filter_tags: list[str] = Field(default_factory=list)
    lifecycle_management_rules_svm_name: str = ""
    lifecycle_management_rules_svm_uuid: str = ""
    lifecycle_management_rules_uuid: OntapUUID = ""


class OntapS3BucketSvmStatement(CacheModel):
    """OntapS3BucketSvmStatement sub-model for statements."""

    policy_statements_actions: list[str] = Field(default_factory=list)
    policy_statements_conditions: list[dict[str, Any]] = Field(default_factory=list)
    policy_statements_effect: str = ""
    policy_statements_principals: list[str] = Field(default_factory=list)
    policy_statements_resources: list[str] = Field(default_factory=list)
    policy_statements_sid: str = ""


class OntapS3BucketSvm(CacheModel):
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
