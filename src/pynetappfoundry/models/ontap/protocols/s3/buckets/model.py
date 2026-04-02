# ruff: noqa: E501
"""OntapS3Bucket information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3BucketAggregate(OntapModel):
    """OntapS3BucketAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketAuditEventSelector(OntapModel):
    """OntapS3BucketAuditEventSelector sub-model for audit_event_selector."""

    access: str = ""
    permission: str = ""


class OntapS3BucketCorsRule(OntapModel):
    """OntapS3BucketCorsRule sub-model for rules."""

    allowed_headers: list[str] = Field(default_factory=list)
    allowed_methods: list[str] = Field(default_factory=list)
    allowed_origins: list[str] = Field(default_factory=list)
    expose_headers: list[str] = Field(default_factory=list)
    id: str = ""
    max_age_seconds: int = 0


class OntapS3BucketCors(OntapModel):
    """OntapS3BucketCors sub-model for cors."""

    rules: list[OntapS3BucketCorsRule] = Field(default_factory=list)


class OntapS3BucketEncryption(OntapModel):
    """OntapS3BucketEncryption sub-model for encryption."""

    enabled: bool = False


class OntapS3BucketLifecycleManagementRuleAbortIncompleteMultipartUpload(OntapModel):
    """OntapS3BucketLifecycleManagementRuleAbortIncompleteMultipartUpload sub-model for abort_incomplete_multipart_upload."""

    after_initiation_days: int = 0


class OntapS3BucketLifecycleManagementRuleExpiration(OntapModel):
    """OntapS3BucketLifecycleManagementRuleExpiration sub-model for expiration."""

    expired_object_delete_marker: bool = False
    object_age_days: int = 0
    object_expiry_date: str = ""


class OntapS3BucketLifecycleManagementRuleNonCurrentVersionExpiration(OntapModel):
    """OntapS3BucketLifecycleManagementRuleNonCurrentVersionExpiration sub-model for non_current_version_expiration."""

    new_non_current_versions: int = 0
    non_current_days: int = 0


class OntapS3BucketLifecycleManagementRuleObjectFilter(OntapModel):
    """OntapS3BucketLifecycleManagementRuleObjectFilter sub-model for object_filter."""

    prefix: str = ""
    size_greater_than: int = 0
    size_less_than: int = 0
    tags: list[str] = Field(default_factory=list)


class OntapS3BucketLifecycleManagementRuleSvm(OntapModel):
    """OntapS3BucketLifecycleManagementRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketLifecycleManagementRule(OntapModel):
    """OntapS3BucketLifecycleManagementRule sub-model for rules."""

    abort_incomplete_multipart_upload: OntapS3BucketLifecycleManagementRuleAbortIncompleteMultipartUpload = Field(
        default_factory=OntapS3BucketLifecycleManagementRuleAbortIncompleteMultipartUpload
    )
    bucket_name: str = ""
    enabled: bool = False
    expiration: OntapS3BucketLifecycleManagementRuleExpiration = Field(
        default_factory=OntapS3BucketLifecycleManagementRuleExpiration
    )
    name: str = ""
    non_current_version_expiration: OntapS3BucketLifecycleManagementRuleNonCurrentVersionExpiration = Field(
        default_factory=OntapS3BucketLifecycleManagementRuleNonCurrentVersionExpiration
    )
    object_filter: OntapS3BucketLifecycleManagementRuleObjectFilter = Field(
        default_factory=OntapS3BucketLifecycleManagementRuleObjectFilter
    )
    svm: OntapS3BucketLifecycleManagementRuleSvm = Field(
        default_factory=OntapS3BucketLifecycleManagementRuleSvm
    )
    uuid: OntapUUID = ""


class OntapS3BucketLifecycleManagement(OntapModel):
    """OntapS3BucketLifecycleManagement sub-model for lifecycle_management."""

    rules: list[OntapS3BucketLifecycleManagementRule] = Field(default_factory=list)


class OntapS3BucketPolicyStatementCondition(OntapModel):
    """OntapS3BucketPolicyStatementCondition sub-model for conditions."""

    delimiters: list[str] = Field(default_factory=list)
    max_keys: list[int] = Field(default_factory=list)
    operator: str = ""
    prefixes: list[str] = Field(default_factory=list)
    source_ips: list[str] = Field(default_factory=list)
    usernames: list[str] = Field(default_factory=list)


class OntapS3BucketPolicyStatement(OntapModel):
    """OntapS3BucketPolicyStatement sub-model for statements."""

    actions: list[str] = Field(default_factory=list)
    conditions: list[OntapS3BucketPolicyStatementCondition] = Field(default_factory=list)
    effect: str = ""
    principals: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapS3BucketPolicy(OntapModel):
    """OntapS3BucketPolicy sub-model for policy."""

    statements: list[OntapS3BucketPolicyStatement] = Field(default_factory=list)


class OntapS3BucketProtectionStatusDestination(OntapModel):
    """OntapS3BucketProtectionStatusDestination sub-model for destination."""

    is_cloud: bool = False
    is_external_cloud: bool = False
    is_ontap: bool = False


class OntapS3BucketProtectionStatus(OntapModel):
    """OntapS3BucketProtectionStatus sub-model for protection_status."""

    destination: OntapS3BucketProtectionStatusDestination = Field(
        default_factory=OntapS3BucketProtectionStatusDestination
    )
    is_protected: bool = False


class OntapS3BucketQosPolicy(OntapModel):
    """OntapS3BucketQosPolicy sub-model for qos_policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapS3BucketRetention(OntapModel):
    """OntapS3BucketRetention sub-model for retention."""

    default_period: str = ""
    mode: str = ""


class OntapS3BucketSnapshotPolicy(OntapModel):
    """OntapS3BucketSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapS3BucketSvm(OntapModel):
    """OntapS3BucketSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketVolume(OntapModel):
    """OntapS3BucketVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapS3Bucket(OntapModel):
    """OntapS3Bucket information."""

    aggregates: list[OntapS3BucketAggregate] = Field(default_factory=list)
    allowed: bool = False
    audit_event_selector: OntapS3BucketAuditEventSelector = Field(
        default_factory=OntapS3BucketAuditEventSelector
    )
    comment: str = ""
    constituents_per_aggregate: int = 0
    cors: OntapS3BucketCors = Field(default_factory=OntapS3BucketCors)
    encryption: OntapS3BucketEncryption = Field(default_factory=OntapS3BucketEncryption)
    lifecycle_management: OntapS3BucketLifecycleManagement = Field(
        default_factory=OntapS3BucketLifecycleManagement
    )
    logical_used_size: int = 0
    name: str = ""
    nas_path: str = ""
    policy: OntapS3BucketPolicy = Field(default_factory=OntapS3BucketPolicy)
    protection_status: OntapS3BucketProtectionStatus = Field(
        default_factory=OntapS3BucketProtectionStatus
    )
    qos_policy: OntapS3BucketQosPolicy = Field(default_factory=OntapS3BucketQosPolicy)
    retention: OntapS3BucketRetention = Field(default_factory=OntapS3BucketRetention)
    role: str = ""
    size: int = 0
    snapshot_policy: OntapS3BucketSnapshotPolicy = Field(
        default_factory=OntapS3BucketSnapshotPolicy
    )
    storage_service_level: str = ""
    svm: OntapS3BucketSvm = Field(default_factory=OntapS3BucketSvm)
    type_: str = ""
    use_mirrored_aggregates: bool = False
    uuid: OntapUUID = ""
    versioning_state: str = ""
    volume: OntapS3BucketVolume = Field(default_factory=OntapS3BucketVolume)
