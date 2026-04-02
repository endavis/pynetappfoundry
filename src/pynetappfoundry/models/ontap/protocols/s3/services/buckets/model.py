# ruff: noqa: E501
"""OntapS3BucketSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3BucketSvmAggregate(OntapModel):
    """OntapS3BucketSvmAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketSvmAuditEventSelector(OntapModel):
    """OntapS3BucketSvmAuditEventSelector sub-model for audit_event_selector."""

    access: str = ""
    permission: str = ""


class OntapS3BucketSvmCorsRule(OntapModel):
    """OntapS3BucketSvmCorsRule sub-model for rules."""

    allowed_headers: list[str] = Field(default_factory=list)
    allowed_methods: list[str] = Field(default_factory=list)
    allowed_origins: list[str] = Field(default_factory=list)
    expose_headers: list[str] = Field(default_factory=list)
    id: str = ""
    max_age_seconds: int = 0


class OntapS3BucketSvmCors(OntapModel):
    """OntapS3BucketSvmCors sub-model for cors."""

    rules: list[OntapS3BucketSvmCorsRule] = Field(default_factory=list)


class OntapS3BucketSvmEncryption(OntapModel):
    """OntapS3BucketSvmEncryption sub-model for encryption."""

    enabled: bool = False


class OntapS3BucketSvmLifecycleManagementRuleAbortIncompleteMultipartUpload(OntapModel):
    """OntapS3BucketSvmLifecycleManagementRuleAbortIncompleteMultipartUpload sub-model for abort_incomplete_multipart_upload."""

    after_initiation_days: int = 0


class OntapS3BucketSvmLifecycleManagementRuleExpiration(OntapModel):
    """OntapS3BucketSvmLifecycleManagementRuleExpiration sub-model for expiration."""

    expired_object_delete_marker: bool = False
    object_age_days: int = 0
    object_expiry_date: str = ""


class OntapS3BucketSvmLifecycleManagementRuleNonCurrentVersionExpiration(OntapModel):
    """OntapS3BucketSvmLifecycleManagementRuleNonCurrentVersionExpiration sub-model for non_current_version_expiration."""

    new_non_current_versions: int = 0
    non_current_days: int = 0


class OntapS3BucketSvmLifecycleManagementRuleObjectFilter(OntapModel):
    """OntapS3BucketSvmLifecycleManagementRuleObjectFilter sub-model for object_filter."""

    prefix: str = ""
    size_greater_than: int = 0
    size_less_than: int = 0
    tags: list[str] = Field(default_factory=list)


class OntapS3BucketSvmLifecycleManagementRuleSvm(OntapModel):
    """OntapS3BucketSvmLifecycleManagementRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketSvmLifecycleManagementRule(OntapModel):
    """OntapS3BucketSvmLifecycleManagementRule sub-model for rules."""

    abort_incomplete_multipart_upload: OntapS3BucketSvmLifecycleManagementRuleAbortIncompleteMultipartUpload = Field(
        default_factory=OntapS3BucketSvmLifecycleManagementRuleAbortIncompleteMultipartUpload
    )
    bucket_name: str = ""
    enabled: bool = False
    expiration: OntapS3BucketSvmLifecycleManagementRuleExpiration = Field(
        default_factory=OntapS3BucketSvmLifecycleManagementRuleExpiration
    )
    name: str = ""
    non_current_version_expiration: OntapS3BucketSvmLifecycleManagementRuleNonCurrentVersionExpiration = Field(
        default_factory=OntapS3BucketSvmLifecycleManagementRuleNonCurrentVersionExpiration
    )
    object_filter: OntapS3BucketSvmLifecycleManagementRuleObjectFilter = Field(
        default_factory=OntapS3BucketSvmLifecycleManagementRuleObjectFilter
    )
    svm: OntapS3BucketSvmLifecycleManagementRuleSvm = Field(
        default_factory=OntapS3BucketSvmLifecycleManagementRuleSvm
    )
    uuid: OntapUUID = ""


class OntapS3BucketSvmLifecycleManagement(OntapModel):
    """OntapS3BucketSvmLifecycleManagement sub-model for lifecycle_management."""

    rules: list[OntapS3BucketSvmLifecycleManagementRule] = Field(default_factory=list)


class OntapS3BucketSvmPolicyStatementCondition(OntapModel):
    """OntapS3BucketSvmPolicyStatementCondition sub-model for conditions."""

    delimiters: list[str] = Field(default_factory=list)
    max_keys: list[int] = Field(default_factory=list)
    operator: str = ""
    prefixes: list[str] = Field(default_factory=list)
    source_ips: list[str] = Field(default_factory=list)
    usernames: list[str] = Field(default_factory=list)


class OntapS3BucketSvmPolicyStatement(OntapModel):
    """OntapS3BucketSvmPolicyStatement sub-model for statements."""

    actions: list[str] = Field(default_factory=list)
    conditions: list[OntapS3BucketSvmPolicyStatementCondition] = Field(default_factory=list)
    effect: str = ""
    principals: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapS3BucketSvmPolicy(OntapModel):
    """OntapS3BucketSvmPolicy sub-model for policy."""

    statements: list[OntapS3BucketSvmPolicyStatement] = Field(default_factory=list)


class OntapS3BucketSvmProtectionStatusDestination(OntapModel):
    """OntapS3BucketSvmProtectionStatusDestination sub-model for destination."""

    is_cloud: bool = False
    is_external_cloud: bool = False
    is_ontap: bool = False


class OntapS3BucketSvmProtectionStatus(OntapModel):
    """OntapS3BucketSvmProtectionStatus sub-model for protection_status."""

    destination: OntapS3BucketSvmProtectionStatusDestination = Field(
        default_factory=OntapS3BucketSvmProtectionStatusDestination
    )
    is_protected: bool = False


class OntapS3BucketSvmQosPolicy(OntapModel):
    """OntapS3BucketSvmQosPolicy sub-model for qos_policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapS3BucketSvmRetention(OntapModel):
    """OntapS3BucketSvmRetention sub-model for retention."""

    default_period: str = ""
    mode: str = ""


class OntapS3BucketSvmSnapshotPolicy(OntapModel):
    """OntapS3BucketSvmSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapS3BucketSvmSvm(OntapModel):
    """OntapS3BucketSvmSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketSvmVolume(OntapModel):
    """OntapS3BucketSvmVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapS3BucketSvm(OntapModel):
    """OntapS3BucketSvm information."""

    aggregates: list[OntapS3BucketSvmAggregate] = Field(default_factory=list)
    audit_event_selector: OntapS3BucketSvmAuditEventSelector = Field(
        default_factory=OntapS3BucketSvmAuditEventSelector
    )
    comment: str = ""
    constituents_per_aggregate: int = 0
    cors: OntapS3BucketSvmCors = Field(default_factory=OntapS3BucketSvmCors)
    encryption: OntapS3BucketSvmEncryption = Field(default_factory=OntapS3BucketSvmEncryption)
    lifecycle_management: OntapS3BucketSvmLifecycleManagement = Field(
        default_factory=OntapS3BucketSvmLifecycleManagement
    )
    logical_used_size: int = 0
    name: str = ""
    nas_path: str = ""
    policy: OntapS3BucketSvmPolicy = Field(default_factory=OntapS3BucketSvmPolicy)
    protection_status: OntapS3BucketSvmProtectionStatus = Field(
        default_factory=OntapS3BucketSvmProtectionStatus
    )
    qos_policy: OntapS3BucketSvmQosPolicy = Field(default_factory=OntapS3BucketSvmQosPolicy)
    retention: OntapS3BucketSvmRetention = Field(default_factory=OntapS3BucketSvmRetention)
    role: str = ""
    size: int = 0
    snapshot_policy: OntapS3BucketSvmSnapshotPolicy = Field(
        default_factory=OntapS3BucketSvmSnapshotPolicy
    )
    storage_service_level: str = ""
    svm: OntapS3BucketSvmSvm = Field(default_factory=OntapS3BucketSvmSvm)
    type_: str = ""
    uuid: OntapUUID = ""
    versioning_state: str = ""
    volume: OntapS3BucketSvmVolume = Field(default_factory=OntapS3BucketSvmVolume)
