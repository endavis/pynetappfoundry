# ruff: noqa: E501
"""OntapS3Service information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapS3ServiceBucketAggregate(OntapModel):
    """OntapS3ServiceBucketAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceBucketAuditEventSelector(OntapModel):
    """OntapS3ServiceBucketAuditEventSelector sub-model for audit_event_selector."""

    access: str = ""
    permission: str = ""


class OntapS3ServiceBucketCorsRule(OntapModel):
    """OntapS3ServiceBucketCorsRule sub-model for rules."""

    allowed_headers: list[str] = Field(default_factory=list)
    allowed_methods: list[str] = Field(default_factory=list)
    allowed_origins: list[str] = Field(default_factory=list)
    expose_headers: list[str] = Field(default_factory=list)
    id: str = ""
    max_age_seconds: int = 0


class OntapS3ServiceBucketCors(OntapModel):
    """OntapS3ServiceBucketCors sub-model for cors."""

    rules: list[OntapS3ServiceBucketCorsRule] = Field(default_factory=list)


class OntapS3ServiceBucketEncryption(OntapModel):
    """OntapS3ServiceBucketEncryption sub-model for encryption."""

    enabled: bool = False


class OntapS3ServiceBucketLifecycleManagementRuleAbortIncompleteMultipartUpload(OntapModel):
    """OntapS3ServiceBucketLifecycleManagementRuleAbortIncompleteMultipartUpload sub-model for abort_incomplete_multipart_upload."""

    after_initiation_days: int = 0


class OntapS3ServiceBucketLifecycleManagementRuleExpiration(OntapModel):
    """OntapS3ServiceBucketLifecycleManagementRuleExpiration sub-model for expiration."""

    expired_object_delete_marker: bool = False
    object_age_days: int = 0
    object_expiry_date: str = ""


class OntapS3ServiceBucketLifecycleManagementRuleNonCurrentVersionExpiration(OntapModel):
    """OntapS3ServiceBucketLifecycleManagementRuleNonCurrentVersionExpiration sub-model for non_current_version_expiration."""

    new_non_current_versions: int = 0
    non_current_days: int = 0


class OntapS3ServiceBucketLifecycleManagementRuleObjectFilter(OntapModel):
    """OntapS3ServiceBucketLifecycleManagementRuleObjectFilter sub-model for object_filter."""

    prefix: str = ""
    size_greater_than: int = 0
    size_less_than: int = 0
    tags: list[str] = Field(default_factory=list)


class OntapS3ServiceBucketLifecycleManagementRuleSvm(OntapModel):
    """OntapS3ServiceBucketLifecycleManagementRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceBucketLifecycleManagementRule(OntapModel):
    """OntapS3ServiceBucketLifecycleManagementRule sub-model for rules."""

    abort_incomplete_multipart_upload: OntapS3ServiceBucketLifecycleManagementRuleAbortIncompleteMultipartUpload = Field(
        default_factory=OntapS3ServiceBucketLifecycleManagementRuleAbortIncompleteMultipartUpload
    )
    bucket_name: str = ""
    enabled: bool = False
    expiration: OntapS3ServiceBucketLifecycleManagementRuleExpiration = Field(
        default_factory=OntapS3ServiceBucketLifecycleManagementRuleExpiration
    )
    name: str = ""
    non_current_version_expiration: OntapS3ServiceBucketLifecycleManagementRuleNonCurrentVersionExpiration = Field(
        default_factory=OntapS3ServiceBucketLifecycleManagementRuleNonCurrentVersionExpiration
    )
    object_filter: OntapS3ServiceBucketLifecycleManagementRuleObjectFilter = Field(
        default_factory=OntapS3ServiceBucketLifecycleManagementRuleObjectFilter
    )
    svm: OntapS3ServiceBucketLifecycleManagementRuleSvm = Field(
        default_factory=OntapS3ServiceBucketLifecycleManagementRuleSvm
    )
    uuid: OntapUUID = ""


class OntapS3ServiceBucketLifecycleManagement(OntapModel):
    """OntapS3ServiceBucketLifecycleManagement sub-model for lifecycle_management."""

    rules: list[OntapS3ServiceBucketLifecycleManagementRule] = Field(default_factory=list)


class OntapS3ServiceBucketPolicyStatementCondition(OntapModel):
    """OntapS3ServiceBucketPolicyStatementCondition sub-model for conditions."""

    delimiters: list[str] = Field(default_factory=list)
    max_keys: list[int] = Field(default_factory=list)
    operator: str = ""
    prefixes: list[str] = Field(default_factory=list)
    source_ips: list[str] = Field(default_factory=list)
    usernames: list[str] = Field(default_factory=list)


class OntapS3ServiceBucketPolicyStatement(OntapModel):
    """OntapS3ServiceBucketPolicyStatement sub-model for statements."""

    actions: list[str] = Field(default_factory=list)
    conditions: list[OntapS3ServiceBucketPolicyStatementCondition] = Field(default_factory=list)
    effect: str = ""
    principals: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapS3ServiceBucketPolicy(OntapModel):
    """OntapS3ServiceBucketPolicy sub-model for policy."""

    statements: list[OntapS3ServiceBucketPolicyStatement] = Field(default_factory=list)


class OntapS3ServiceBucketProtectionStatusDestination(OntapModel):
    """OntapS3ServiceBucketProtectionStatusDestination sub-model for destination."""

    is_cloud: bool = False
    is_external_cloud: bool = False
    is_ontap: bool = False


class OntapS3ServiceBucketProtectionStatus(OntapModel):
    """OntapS3ServiceBucketProtectionStatus sub-model for protection_status."""

    destination: OntapS3ServiceBucketProtectionStatusDestination = Field(
        default_factory=OntapS3ServiceBucketProtectionStatusDestination
    )
    is_protected: bool = False


class OntapS3ServiceBucketQosPolicy(OntapModel):
    """OntapS3ServiceBucketQosPolicy sub-model for qos_policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapS3ServiceBucketRetention(OntapModel):
    """OntapS3ServiceBucketRetention sub-model for retention."""

    default_period: str = ""
    mode: str = ""


class OntapS3ServiceBucketSnapshotPolicy(OntapModel):
    """OntapS3ServiceBucketSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapS3ServiceBucketSvm(OntapModel):
    """OntapS3ServiceBucketSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceBucketVolume(OntapModel):
    """OntapS3ServiceBucketVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceBucket(OntapModel):
    """OntapS3ServiceBucket sub-model for buckets."""

    aggregates: list[OntapS3ServiceBucketAggregate] = Field(default_factory=list)
    allowed: bool = False
    audit_event_selector: OntapS3ServiceBucketAuditEventSelector = Field(
        default_factory=OntapS3ServiceBucketAuditEventSelector
    )
    comment: str = ""
    constituents_per_aggregate: int = 0
    cors: OntapS3ServiceBucketCors = Field(default_factory=OntapS3ServiceBucketCors)
    encryption: OntapS3ServiceBucketEncryption = Field(
        default_factory=OntapS3ServiceBucketEncryption
    )
    lifecycle_management: OntapS3ServiceBucketLifecycleManagement = Field(
        default_factory=OntapS3ServiceBucketLifecycleManagement
    )
    logical_used_size: int = 0
    name: str = ""
    nas_path: str = ""
    policy: OntapS3ServiceBucketPolicy = Field(default_factory=OntapS3ServiceBucketPolicy)
    protection_status: OntapS3ServiceBucketProtectionStatus = Field(
        default_factory=OntapS3ServiceBucketProtectionStatus
    )
    qos_policy: OntapS3ServiceBucketQosPolicy = Field(default_factory=OntapS3ServiceBucketQosPolicy)
    retention: OntapS3ServiceBucketRetention = Field(default_factory=OntapS3ServiceBucketRetention)
    role: str = ""
    size: int = 0
    snapshot_policy: OntapS3ServiceBucketSnapshotPolicy = Field(
        default_factory=OntapS3ServiceBucketSnapshotPolicy
    )
    storage_service_level: str = ""
    svm: OntapS3ServiceBucketSvm = Field(default_factory=OntapS3ServiceBucketSvm)
    type_: str = ""
    use_mirrored_aggregates: bool = False
    uuid: OntapUUID = ""
    versioning_state: str = ""
    volume: OntapS3ServiceBucketVolume = Field(default_factory=OntapS3ServiceBucketVolume)


class OntapS3ServiceCertificate(OntapModel):
    """OntapS3ServiceCertificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceMetricIops(OntapModel):
    """OntapS3ServiceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapS3ServiceMetricLatency(OntapModel):
    """OntapS3ServiceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapS3ServiceMetricThroughput(OntapModel):
    """OntapS3ServiceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapS3ServiceMetric(OntapModel):
    """OntapS3ServiceMetric sub-model for metric."""

    duration: str = ""
    iops: OntapS3ServiceMetricIops = Field(default_factory=OntapS3ServiceMetricIops)
    latency: OntapS3ServiceMetricLatency = Field(default_factory=OntapS3ServiceMetricLatency)
    status: str = ""
    throughput: OntapS3ServiceMetricThroughput = Field(
        default_factory=OntapS3ServiceMetricThroughput
    )
    timestamp: str = ""


class OntapS3ServiceStatisticsIopsRaw(OntapModel):
    """OntapS3ServiceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapS3ServiceStatisticsLatencyRaw(OntapModel):
    """OntapS3ServiceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapS3ServiceStatisticsThroughputRaw(OntapModel):
    """OntapS3ServiceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapS3ServiceStatistics(OntapModel):
    """OntapS3ServiceStatistics sub-model for statistics."""

    iops_raw: OntapS3ServiceStatisticsIopsRaw = Field(
        default_factory=OntapS3ServiceStatisticsIopsRaw
    )
    latency_raw: OntapS3ServiceStatisticsLatencyRaw = Field(
        default_factory=OntapS3ServiceStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapS3ServiceStatisticsThroughputRaw = Field(
        default_factory=OntapS3ServiceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapS3ServiceSvm(OntapModel):
    """OntapS3ServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceUserSvm(OntapModel):
    """OntapS3ServiceUserSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3ServiceUser(OntapModel):
    """OntapS3ServiceUser sub-model for users."""

    access_key: str = ""
    comment: str = ""
    key_expiry_time: str = ""
    key_time_to_live: str = ""
    name: str = ""
    secret_key: str = ""
    svm: OntapS3ServiceUserSvm = Field(default_factory=OntapS3ServiceUserSvm)


class OntapS3Service(OntapModel):
    """OntapS3Service information."""

    buckets: list[OntapS3ServiceBucket] = Field(default_factory=list)
    certificate: OntapS3ServiceCertificate = Field(default_factory=OntapS3ServiceCertificate)
    comment: str = ""
    default_unix_user: str = ""
    default_win_user: str = ""
    enabled: bool = False
    is_http_enabled: bool = False
    is_https_enabled: bool = False
    max_key_time_to_live: str = ""
    max_lock_retention_period: str = ""
    metric: OntapS3ServiceMetric = Field(default_factory=OntapS3ServiceMetric)
    min_lock_retention_period: str = ""
    name: str = ""
    port: int = 0
    secure_port: int = 0
    statistics: OntapS3ServiceStatistics = Field(default_factory=OntapS3ServiceStatistics)
    svm: OntapS3ServiceSvm = Field(default_factory=OntapS3ServiceSvm)
    users: list[OntapS3ServiceUser] = Field(default_factory=list)
