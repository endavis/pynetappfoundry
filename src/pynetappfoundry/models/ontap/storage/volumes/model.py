# ruff: noqa: E501
"""OntapVolume information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVolumeActivityTrackingUnsupportedReason(OntapModel):
    """OntapVolumeActivityTrackingUnsupportedReason sub-model for unsupported_reason."""

    code: str = ""
    message: str = ""


class OntapVolumeActivityTracking(OntapModel):
    """OntapVolumeActivityTracking sub-model for activity_tracking."""

    state: str = ""
    supported: bool = False
    unsupported_reason: OntapVolumeActivityTrackingUnsupportedReason = Field(
        default_factory=OntapVolumeActivityTrackingUnsupportedReason
    )


class OntapVolumeAggregate(OntapModel):
    """OntapVolumeAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapVolumeAnalyticsInitialization(OntapModel):
    """OntapVolumeAnalyticsInitialization sub-model for initialization."""

    state: str = ""


class OntapVolumeAnalyticsScanThrottleReason(OntapModel):
    """OntapVolumeAnalyticsScanThrottleReason sub-model for scan_throttle_reason."""

    arguments: list[str] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapVolumeAnalyticsUnsupportedReason(OntapModel):
    """OntapVolumeAnalyticsUnsupportedReason sub-model for unsupported_reason."""

    code: str = ""
    message: str = ""


class OntapVolumeAnalytics(OntapModel):
    """OntapVolumeAnalytics sub-model for analytics."""

    files_scanned: int = 0
    initialization: OntapVolumeAnalyticsInitialization = Field(
        default_factory=OntapVolumeAnalyticsInitialization
    )
    scan_progress: int = 0
    scan_throttle_reason: OntapVolumeAnalyticsScanThrottleReason = Field(
        default_factory=OntapVolumeAnalyticsScanThrottleReason
    )
    state: str = ""
    supported: bool = False
    total_files: int = 0
    unsupported_reason: OntapVolumeAnalyticsUnsupportedReason = Field(
        default_factory=OntapVolumeAnalyticsUnsupportedReason
    )


class OntapVolumeAntiRansomwareAttackDetectionParameters(OntapModel):
    """OntapVolumeAntiRansomwareAttackDetectionParameters sub-model for attack_detection_parameters."""

    based_on_file_create_op_rate: bool = False
    based_on_file_delete_op_rate: bool = False
    based_on_file_rename_op_rate: bool = False
    based_on_high_entropy_data_rate: bool = False
    based_on_never_seen_before_file_extension: bool = False
    file_create_op_rate_surge_notify_percent: int = 0
    file_delete_op_rate_surge_notify_percent: int = 0
    file_rename_op_rate_surge_notify_percent: int = 0
    high_entropy_data_surge_notify_percent: int = 0
    never_seen_before_file_extension_count_notify_threshold: int = 0
    never_seen_before_file_extension_duration_in_hours: int = 0
    relaxing_popular_file_extensions: bool = False


class OntapVolumeAntiRansomwareAttackReport(OntapModel):
    """OntapVolumeAntiRansomwareAttackReport sub-model for attack_reports."""

    time: str = ""


class OntapVolumeAntiRansomwareEventLog(OntapModel):
    """OntapVolumeAntiRansomwareEventLog sub-model for event_log."""

    is_enabled_on_new_file_extension_seen: bool = False
    is_enabled_on_snapshot_copy_creation: bool = False


class OntapVolumeAntiRansomwareSpace(OntapModel):
    """OntapVolumeAntiRansomwareSpace sub-model for space."""

    snapshot_count: int = 0
    used: int = 0
    used_by_logs: int = 0
    used_by_snapshots: int = 0


class OntapVolumeAntiRansomwareSurgeUsage(OntapModel):
    """OntapVolumeAntiRansomwareSurgeUsage sub-model for surge_usage."""

    file_create_peak_rate_per_minute: int = 0
    file_delete_peak_rate_per_minute: int = 0
    file_rename_peak_rate_per_minute: int = 0
    high_entropy_data_write_peak_percent: int = 0
    high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    time: str = ""


class OntapVolumeAntiRansomwareSuspectFile(OntapModel):
    """OntapVolumeAntiRansomwareSuspectFile sub-model for suspect_files."""

    count: int = 0
    entropy: str = ""
    format: str = ""


class OntapVolumeAntiRansomwareTypicalUsage(OntapModel):
    """OntapVolumeAntiRansomwareTypicalUsage sub-model for typical_usage."""

    file_create_peak_rate_per_minute: int = 0
    file_delete_peak_rate_per_minute: int = 0
    file_rename_peak_rate_per_minute: int = 0
    high_entropy_data_write_peak_percent: int = 0
    high_entropy_data_write_peak_rate_kb_per_minute: int = 0


class OntapVolumeAntiRansomwareWorkloadHistoricalStatistics(OntapModel):
    """OntapVolumeAntiRansomwareWorkloadHistoricalStatistics sub-model for historical_statistics."""

    file_create_peak_rate_per_minute: int = 0
    file_delete_peak_rate_per_minute: int = 0
    file_rename_peak_rate_per_minute: int = 0
    high_entropy_data_write_peak_percent: int = 0
    high_entropy_data_write_peak_rate_kb_per_minute: int = 0


class OntapVolumeAntiRansomwareWorkloadNewlyObservedFileExtension(OntapModel):
    """OntapVolumeAntiRansomwareWorkloadNewlyObservedFileExtension sub-model for newly_observed_file_extensions."""

    count: int = 0
    name: str = ""


class OntapVolumeAntiRansomwareWorkloadSurgeStatistics(OntapModel):
    """OntapVolumeAntiRansomwareWorkloadSurgeStatistics sub-model for surge_statistics."""

    file_create_peak_rate_per_minute: int = 0
    file_delete_peak_rate_per_minute: int = 0
    file_rename_peak_rate_per_minute: int = 0
    high_entropy_data_write_peak_percent: int = 0
    high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    time: str = ""


class OntapVolumeAntiRansomwareWorkloadSurgeUsageNewlyObservedFileExtension(OntapModel):
    """OntapVolumeAntiRansomwareWorkloadSurgeUsageNewlyObservedFileExtension sub-model for newly_observed_file_extensions."""

    count: int = 0
    name: str = ""


class OntapVolumeAntiRansomwareWorkloadSurgeUsage(OntapModel):
    """OntapVolumeAntiRansomwareWorkloadSurgeUsage sub-model for surge_usage."""

    file_create_peak_rate_per_minute: int = 0
    file_delete_peak_rate_per_minute: int = 0
    file_rename_peak_rate_per_minute: int = 0
    high_entropy_data_write_peak_percent: int = 0
    high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    newly_observed_file_extensions: list[
        OntapVolumeAntiRansomwareWorkloadSurgeUsageNewlyObservedFileExtension
    ] = Field(default_factory=list)
    time: str = ""


class OntapVolumeAntiRansomwareWorkloadTypicalUsage(OntapModel):
    """OntapVolumeAntiRansomwareWorkloadTypicalUsage sub-model for typical_usage."""

    file_create_peak_rate_per_minute: int = 0
    file_delete_peak_rate_per_minute: int = 0
    file_rename_peak_rate_per_minute: int = 0
    high_entropy_data_write_peak_percent: int = 0
    high_entropy_data_write_peak_rate_kb_per_minute: int = 0


class OntapVolumeAntiRansomwareWorkload(OntapModel):
    """OntapVolumeAntiRansomwareWorkload sub-model for workload."""

    file_extension_types_count: int = 0
    file_extensions_observed: list[str] = Field(default_factory=list)
    historical_statistics: OntapVolumeAntiRansomwareWorkloadHistoricalStatistics = Field(
        default_factory=OntapVolumeAntiRansomwareWorkloadHistoricalStatistics
    )
    newly_observed_file_extensions: list[
        OntapVolumeAntiRansomwareWorkloadNewlyObservedFileExtension
    ] = Field(default_factory=list)
    surge_statistics: OntapVolumeAntiRansomwareWorkloadSurgeStatistics = Field(
        default_factory=OntapVolumeAntiRansomwareWorkloadSurgeStatistics
    )
    surge_usage: OntapVolumeAntiRansomwareWorkloadSurgeUsage = Field(
        default_factory=OntapVolumeAntiRansomwareWorkloadSurgeUsage
    )
    typical_usage: OntapVolumeAntiRansomwareWorkloadTypicalUsage = Field(
        default_factory=OntapVolumeAntiRansomwareWorkloadTypicalUsage
    )


class OntapVolumeAntiRansomware(OntapModel):
    """OntapVolumeAntiRansomware sub-model for anti_ransomware."""

    attack_detection_parameters: OntapVolumeAntiRansomwareAttackDetectionParameters = Field(
        default_factory=OntapVolumeAntiRansomwareAttackDetectionParameters
    )
    attack_probability: str = ""
    attack_reports: list[OntapVolumeAntiRansomwareAttackReport] = Field(default_factory=list)
    dry_run_start_time: str = ""
    event_log: OntapVolumeAntiRansomwareEventLog = Field(
        default_factory=OntapVolumeAntiRansomwareEventLog
    )
    space: OntapVolumeAntiRansomwareSpace = Field(default_factory=OntapVolumeAntiRansomwareSpace)
    state: str = ""
    surge_as_normal: bool = False
    surge_usage: OntapVolumeAntiRansomwareSurgeUsage = Field(
        default_factory=OntapVolumeAntiRansomwareSurgeUsage
    )
    suspect_files: list[OntapVolumeAntiRansomwareSuspectFile] = Field(default_factory=list)
    typical_usage: OntapVolumeAntiRansomwareTypicalUsage = Field(
        default_factory=OntapVolumeAntiRansomwareTypicalUsage
    )
    update_baseline_from_surge: bool = False
    workload: OntapVolumeAntiRansomwareWorkload = Field(
        default_factory=OntapVolumeAntiRansomwareWorkload
    )


class OntapVolumeApplication(OntapModel):
    """OntapVolumeApplication sub-model for application."""

    name: str = ""
    uuid: str = ""


class OntapVolumeAsynchronousDirectoryDelete(OntapModel):
    """OntapVolumeAsynchronousDirectoryDelete sub-model for asynchronous_directory_delete."""

    enabled: bool = False
    trash_bin: str = ""


class OntapVolumeAutosize(OntapModel):
    """OntapVolumeAutosize sub-model for autosize."""

    grow_threshold: int = 0
    maximum: int = 0
    minimum: int = 0
    mode: str = ""
    shrink_threshold: int = 0


class OntapVolumeCloneParentSnapshot(OntapModel):
    """OntapVolumeCloneParentSnapshot sub-model for parent_snapshot."""

    name: str = ""
    uuid: str = ""


class OntapVolumeCloneParentSvm(OntapModel):
    """OntapVolumeCloneParentSvm sub-model for parent_svm."""

    name: str = ""
    uuid: str = ""


class OntapVolumeCloneParentVolume(OntapModel):
    """OntapVolumeCloneParentVolume sub-model for parent_volume."""

    name: str = ""
    uuid: str = ""


class OntapVolumeClone(OntapModel):
    """OntapVolumeClone sub-model for clone."""

    has_flexclone: bool = False
    inherited_physical_used: int = 0
    inherited_savings: int = 0
    is_flexclone: bool = False
    parent_snapshot: OntapVolumeCloneParentSnapshot = Field(
        default_factory=OntapVolumeCloneParentSnapshot
    )
    parent_svm: OntapVolumeCloneParentSvm = Field(default_factory=OntapVolumeCloneParentSvm)
    parent_volume: OntapVolumeCloneParentVolume = Field(
        default_factory=OntapVolumeCloneParentVolume
    )
    split_complete_percent: int = 0
    split_estimate: int = 0
    split_initiated: bool = False


class OntapVolumeConsistencyGroup(OntapModel):
    """OntapVolumeConsistencyGroup sub-model for consistency_group."""

    name: str = ""
    uuid: str = ""


class OntapVolumeConstituentAggregates(OntapModel):
    """OntapVolumeConstituentAggregates sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapVolumeConstituentMovementDestinationAggregate(OntapModel):
    """OntapVolumeConstituentMovementDestinationAggregate sub-model for destination_aggregate."""

    name: str = ""
    uuid: str = ""


class OntapVolumeConstituentMovement(OntapModel):
    """OntapVolumeConstituentMovement sub-model for movement."""

    cutover_window: int = 0
    destination_aggregate: OntapVolumeConstituentMovementDestinationAggregate = Field(
        default_factory=OntapVolumeConstituentMovementDestinationAggregate
    )
    percent_complete: int = 0
    state: str = ""
    tiering_policy: str = ""


class OntapVolumeConstituentSpaceLogicalSpace(OntapModel):
    """OntapVolumeConstituentSpaceLogicalSpace sub-model for logical_space."""

    available: int = 0
    enforcement: bool = False
    reporting: bool = False
    used_by_afs: int = 0


class OntapVolumeConstituentSpaceSnapshot(OntapModel):
    """OntapVolumeConstituentSpaceSnapshot sub-model for snapshot."""

    autodelete_enabled: bool = False
    reserve_percent: int = 0
    used: int = 0


class OntapVolumeConstituentSpace(OntapModel):
    """OntapVolumeConstituentSpace sub-model for space."""

    afs_total: int = 0
    available: int = 0
    available_percent: int = 0
    block_storage_inactive_user_data: int = 0
    capacity_tier_footprint: int = 0
    footprint: int = 0
    large_size_enabled: bool = False
    local_tier_footprint: int = 0
    logical_space: OntapVolumeConstituentSpaceLogicalSpace = Field(
        default_factory=OntapVolumeConstituentSpaceLogicalSpace
    )
    max_size: str = ""
    metadata_: int = 0
    over_provisioned: int = 0
    performance_tier_footprint: int = 0
    size: int = 0
    snapshot: OntapVolumeConstituentSpaceSnapshot = Field(
        default_factory=OntapVolumeConstituentSpaceSnapshot
    )
    total_footprint: int = 0
    total_metadata: int = 0
    total_metadata_footprint: int = 0
    used: int = 0
    used_by_afs: int = 0
    used_percent: int = 0


class OntapVolumeConstituent(OntapModel):
    """OntapVolumeConstituent sub-model for constituents."""

    aggregates: OntapVolumeConstituentAggregates = Field(
        default_factory=OntapVolumeConstituentAggregates
    )
    movement: OntapVolumeConstituentMovement = Field(default_factory=OntapVolumeConstituentMovement)
    name: str = ""
    space: OntapVolumeConstituentSpace = Field(default_factory=OntapVolumeConstituentSpace)


class OntapVolumeEfficiencyIdcsScanner(OntapModel):
    """OntapVolumeEfficiencyIdcsScanner sub-model for idcs_scanner."""

    enabled: bool = False
    inactive_days: int = 0
    mode: str = ""
    operation_state: str = ""
    status: str = ""
    threshold_inactive_time: str = ""


class OntapVolumeEfficiencyPolicy(OntapModel):
    """OntapVolumeEfficiencyPolicy sub-model for policy."""

    name: str = ""


class OntapVolumeEfficiencyScanner(OntapModel):
    """OntapVolumeEfficiencyScanner sub-model for scanner."""

    compression: bool = False
    dedupe: bool = False
    scan_old_data: bool = False
    state: str = ""


class OntapVolumeEfficiencySpaceSavings(OntapModel):
    """OntapVolumeEfficiencySpaceSavings sub-model for space_savings."""

    compression: int = 0
    compression_percent: int = 0
    dedupe: int = 0
    dedupe_percent: int = 0
    dedupe_sharing: int = 0
    total: int = 0
    total_percent: int = 0


class OntapVolumeEfficiency(OntapModel):
    """OntapVolumeEfficiency sub-model for efficiency."""

    application_io_size: str = ""
    auto_state: str = ""
    compaction: str = ""
    compression: str = ""
    compression_type: str = ""
    cross_volume_dedupe: str = ""
    dedupe: str = ""
    has_savings: bool = False
    idcs_scanner: OntapVolumeEfficiencyIdcsScanner = Field(
        default_factory=OntapVolumeEfficiencyIdcsScanner
    )
    last_op_begin: str = ""
    last_op_end: str = ""
    last_op_err: str = ""
    last_op_size: int = 0
    last_op_state: str = ""
    logging_enabled: bool = False
    op_state: str = ""
    policy: OntapVolumeEfficiencyPolicy = Field(default_factory=OntapVolumeEfficiencyPolicy)
    progress: str = ""
    scanner: OntapVolumeEfficiencyScanner = Field(default_factory=OntapVolumeEfficiencyScanner)
    schedule: str = ""
    space_savings: OntapVolumeEfficiencySpaceSavings = Field(
        default_factory=OntapVolumeEfficiencySpaceSavings
    )
    state: str = ""
    storage_efficiency_mode: str = ""
    type_: str = ""
    volume_path: str = ""


class OntapVolumeEncryptionStatus(OntapModel):
    """OntapVolumeEncryptionStatus sub-model for status."""

    code: str = ""
    message: str = ""


class OntapVolumeEncryption(OntapModel):
    """OntapVolumeEncryption sub-model for encryption."""

    action: str = ""
    enabled: bool = False
    key_create_time: str = ""
    key_id: str = ""
    key_manager_attribute: str = ""
    rekey: bool = False
    state: str = ""
    status: OntapVolumeEncryptionStatus = Field(default_factory=OntapVolumeEncryptionStatus)
    type_: str = ""


class OntapVolumeErrorState(OntapModel):
    """OntapVolumeErrorState sub-model for error_state."""

    has_bad_blocks: bool = False
    is_inconsistent: bool = False


class OntapVolumeFiles(OntapModel):
    """OntapVolumeFiles sub-model for files."""

    maximum: int = 0
    used: int = 0


class OntapVolumeFlashPool(OntapModel):
    """OntapVolumeFlashPool sub-model for flash_pool."""

    cache_eligibility: str = ""
    cache_retention_priority: str = ""
    caching_policy: str = ""


class OntapVolumeFlexgroup(OntapModel):
    """OntapVolumeFlexgroup sub-model for flexgroup."""

    name: str = ""
    uuid: str = ""


class OntapVolumeGuarantee(OntapModel):
    """OntapVolumeGuarantee sub-model for guarantee."""

    honored: bool = False
    type_: str = ""


class OntapVolumeMetricCloudIops(OntapModel):
    """OntapVolumeMetricCloudIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricCloudLatency(OntapModel):
    """OntapVolumeMetricCloudLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricCloud(OntapModel):
    """OntapVolumeMetricCloud sub-model for cloud."""

    duration: str = ""
    iops: OntapVolumeMetricCloudIops = Field(default_factory=OntapVolumeMetricCloudIops)
    latency: OntapVolumeMetricCloudLatency = Field(default_factory=OntapVolumeMetricCloudLatency)
    status: str = ""
    timestamp: str = ""


class OntapVolumeMetricFlexcache(OntapModel):
    """OntapVolumeMetricFlexcache sub-model for flexcache."""

    bandwidth_savings: int = 0
    cache_miss_percent: int = 0
    duration: str = ""
    status: str = ""
    timestamp: str = ""


class OntapVolumeMetricIops(OntapModel):
    """OntapVolumeMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricLatency(OntapModel):
    """OntapVolumeMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricThroughput(OntapModel):
    """OntapVolumeMetricThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetric(OntapModel):
    """OntapVolumeMetric sub-model for metric."""

    cloud: OntapVolumeMetricCloud = Field(default_factory=OntapVolumeMetricCloud)
    duration: str = ""
    flexcache: OntapVolumeMetricFlexcache = Field(default_factory=OntapVolumeMetricFlexcache)
    iops: OntapVolumeMetricIops = Field(default_factory=OntapVolumeMetricIops)
    latency: OntapVolumeMetricLatency = Field(default_factory=OntapVolumeMetricLatency)
    status: str = ""
    throughput: OntapVolumeMetricThroughput = Field(default_factory=OntapVolumeMetricThroughput)
    timestamp: str = ""


class OntapVolumeMovementDestinationAggregate(OntapModel):
    """OntapVolumeMovementDestinationAggregate sub-model for destination_aggregate."""

    name: str = ""
    uuid: str = ""


class OntapVolumeMovement(OntapModel):
    """OntapVolumeMovement sub-model for movement."""

    capacity_tier_optimized: bool = False
    cutover_window: int = 0
    destination_aggregate: OntapVolumeMovementDestinationAggregate = Field(
        default_factory=OntapVolumeMovementDestinationAggregate
    )
    percent_complete: int = 0
    start_time: str = ""
    state: str = ""
    tiering_policy: str = ""


class OntapVolumeNasExportPolicy(OntapModel):
    """OntapVolumeNasExportPolicy sub-model for export_policy."""

    id: int = 0
    name: str = ""


class OntapVolumeNasJunctionParent(OntapModel):
    """OntapVolumeNasJunctionParent sub-model for junction_parent."""

    name: str = ""
    uuid: str = ""


class OntapVolumeNas(OntapModel):
    """OntapVolumeNas sub-model for nas."""

    export_policy: OntapVolumeNasExportPolicy = Field(default_factory=OntapVolumeNasExportPolicy)
    gid: int = 0
    junction_parent: OntapVolumeNasJunctionParent = Field(
        default_factory=OntapVolumeNasJunctionParent
    )
    path: str = ""
    security_style: str = ""
    uid: int = 0
    unix_permissions: int = 0


class OntapVolumeQosPolicy(OntapModel):
    """OntapVolumeQosPolicy sub-model for policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapVolumeQos(OntapModel):
    """OntapVolumeQos sub-model for qos."""

    policy: OntapVolumeQosPolicy = Field(default_factory=OntapVolumeQosPolicy)


class OntapVolumeQuota(OntapModel):
    """OntapVolumeQuota sub-model for quota."""

    enabled: bool = False
    state: str = ""


class OntapVolumeRebalancingEngineMovementLastError(OntapModel):
    """OntapVolumeRebalancingEngineMovementLastError sub-model for last_error."""

    code: int = 0
    destination: int = 0
    file_id: int = 0
    time: str = ""


class OntapVolumeRebalancingEngineMovement(OntapModel):
    """OntapVolumeRebalancingEngineMovement sub-model for movement."""

    file_moves_started: int = 0
    last_error: OntapVolumeRebalancingEngineMovementLastError = Field(
        default_factory=OntapVolumeRebalancingEngineMovementLastError
    )
    most_recent_start_time: str = ""


class OntapVolumeRebalancingEngineScannerBlocksSkipped(OntapModel):
    """OntapVolumeRebalancingEngineScannerBlocksSkipped sub-model for blocks_skipped."""

    efficiency_blocks: int = 0
    efficiency_percent: int = 0
    fast_truncate: int = 0
    footprint_invalid: int = 0
    in_snapshot: int = 0
    incompatible: int = 0
    metadata_: int = 0
    on_demand_destination: int = 0
    other: int = 0
    remote_cache: int = 0
    too_large: int = 0
    too_small: int = 0
    write_fenced: int = 0


class OntapVolumeRebalancingEngineScannerFilesSkipped(OntapModel):
    """OntapVolumeRebalancingEngineScannerFilesSkipped sub-model for files_skipped."""

    efficiency_blocks: int = 0
    efficiency_percent: int = 0
    fast_truncate: int = 0
    footprint_invalid: int = 0
    in_snapshot: int = 0
    incompatible: int = 0
    metadata_: int = 0
    on_demand_destination: int = 0
    other: int = 0
    remote_cache: int = 0
    too_large: int = 0
    too_small: int = 0
    write_fenced: int = 0


class OntapVolumeRebalancingEngineScanner(OntapModel):
    """OntapVolumeRebalancingEngineScanner sub-model for scanner."""

    blocks_scanned: int = 0
    blocks_skipped: OntapVolumeRebalancingEngineScannerBlocksSkipped = Field(
        default_factory=OntapVolumeRebalancingEngineScannerBlocksSkipped
    )
    files_scanned: int = 0
    files_skipped: OntapVolumeRebalancingEngineScannerFilesSkipped = Field(
        default_factory=OntapVolumeRebalancingEngineScannerFilesSkipped
    )


class OntapVolumeRebalancingEngine(OntapModel):
    """OntapVolumeRebalancingEngine sub-model for engine."""

    movement: OntapVolumeRebalancingEngineMovement = Field(
        default_factory=OntapVolumeRebalancingEngineMovement
    )
    scanner: OntapVolumeRebalancingEngineScanner = Field(
        default_factory=OntapVolumeRebalancingEngineScanner
    )


class OntapVolumeRebalancingNoticeArgument(OntapModel):
    """OntapVolumeRebalancingNoticeArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapVolumeRebalancingNotice(OntapModel):
    """OntapVolumeRebalancingNotice sub-model for notices."""

    arguments: list[OntapVolumeRebalancingNoticeArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapVolumeRebalancing(OntapModel):
    """OntapVolumeRebalancing sub-model for rebalancing."""

    data_moved: int = 0
    engine: OntapVolumeRebalancingEngine = Field(default_factory=OntapVolumeRebalancingEngine)
    exclude_snapshots: bool = False
    imbalance_percent: int = 0
    imbalance_size: int = 0
    max_constituent_imbalance_percent: int = 0
    max_file_moves: int = 0
    max_runtime: str = ""
    max_threshold: int = 0
    min_file_size: int = 0
    min_threshold: int = 0
    notices: list[OntapVolumeRebalancingNotice] = Field(default_factory=list)
    runtime: str = ""
    start_time: str = ""
    state: str = ""
    stop_time: str = ""
    target_used: int = 0
    used_for_imbalance: int = 0


class OntapVolumeSnaplockRetention(OntapModel):
    """OntapVolumeSnaplockRetention sub-model for retention."""

    default: str = ""
    maximum: str = ""
    minimum: str = ""


class OntapVolumeSnaplock(OntapModel):
    """OntapVolumeSnaplock sub-model for snaplock."""

    append_mode_enabled: bool = False
    autocommit_period: str = ""
    compliance_clock_time: str = ""
    expiry_time: str = ""
    is_audit_log: bool = False
    litigation_count: int = 0
    privileged_delete: str = ""
    retention: OntapVolumeSnaplockRetention = Field(default_factory=OntapVolumeSnaplockRetention)
    type_: str = ""
    unspecified_retention_file_count: int = 0


class OntapVolumeSnapmirrorDestinations(OntapModel):
    """OntapVolumeSnapmirrorDestinations sub-model for destinations."""

    is_cloud: bool = False
    is_ontap: bool = False


class OntapVolumeSnapmirror(OntapModel):
    """OntapVolumeSnapmirror sub-model for snapmirror."""

    destinations: OntapVolumeSnapmirrorDestinations = Field(
        default_factory=OntapVolumeSnapmirrorDestinations
    )
    is_protected: bool = False


class OntapVolumeSnapshotPolicy(OntapModel):
    """OntapVolumeSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapVolumeSpaceLogicalSpace(OntapModel):
    """OntapVolumeSpaceLogicalSpace sub-model for logical_space."""

    available: int = 0
    enforcement: bool = False
    reporting: bool = False
    used: int = 0
    used_by_afs: int = 0
    used_by_snapshots: int = 0
    used_percent: int = 0


class OntapVolumeSpaceSnapshotAutodelete(OntapModel):
    """OntapVolumeSpaceSnapshotAutodelete sub-model for autodelete."""

    commitment: str = ""
    defer_delete: str = ""
    delete_order: str = ""
    enabled: bool = False
    prefix: str = ""
    target_free_space: int = 0
    trigger: str = ""


class OntapVolumeSpaceSnapshot(OntapModel):
    """OntapVolumeSpaceSnapshot sub-model for snapshot."""

    autodelete: OntapVolumeSpaceSnapshotAutodelete = Field(
        default_factory=OntapVolumeSpaceSnapshotAutodelete
    )
    autodelete_enabled: bool = False
    autodelete_trigger: str = ""
    reserve_available: int = 0
    reserve_percent: int = 0
    reserve_size: int = 0
    space_used_percent: int = 0
    used: int = 0


class OntapVolumeSpace(OntapModel):
    """OntapVolumeSpace sub-model for space."""

    afs_total: int = 0
    auto_adaptive_compression_footprint_data_reduction: int = 0
    available: int = 0
    available_percent: int = 0
    block_storage_inactive_user_data: int = 0
    block_storage_inactive_user_data_percent: int = 0
    capacity_tier_footprint: int = 0
    capacity_tier_footprint_data_reduction: int = 0
    compaction_footprint_data_reduction: int = 0
    cross_volume_dedupe_metafiles_footprint: int = 0
    cross_volume_dedupe_metafiles_temporary_footprint: int = 0
    dedupe_metafiles_footprint: int = 0
    dedupe_metafiles_temporary_footprint: int = 0
    delayed_free_footprint: int = 0
    effective_total_footprint: int = 0
    expected_available: int = 0
    file_operation_metadata: int = 0
    filesystem_size: int = 0
    filesystem_size_fixed: bool = False
    footprint: int = 0
    fractional_reserve: int = 0
    full_threshold_percent: int = 0
    is_used_stale: bool = False
    large_size_enabled: bool = False
    local_tier_footprint: int = 0
    logical_space: OntapVolumeSpaceLogicalSpace = Field(
        default_factory=OntapVolumeSpaceLogicalSpace
    )
    max_size: str = ""
    metadata_: int = 0
    nearly_full_threshold_percent: int = 0
    over_provisioned: int = 0
    overwrite_reserve: int = 0
    overwrite_reserve_used: int = 0
    percent_used: int = 0
    performance_tier_footprint: int = 0
    physical_used: int = 0
    physical_used_percent: int = 0
    size: int = 0
    size_available_for_snapshots: int = 0
    snapmirror_destination_footprint: int = 0
    snapshot: OntapVolumeSpaceSnapshot = Field(default_factory=OntapVolumeSpaceSnapshot)
    snapshot_reserve_unusable: int = 0
    snapshot_spill: int = 0
    total_footprint: int = 0
    total_metadata: int = 0
    total_metadata_footprint: int = 0
    used: int = 0
    used_by_afs: int = 0
    user_data: int = 0
    volume_guarantee_footprint: int = 0


class OntapVolumeStatisticsCifsOpsRawAccess(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawAccess sub-model for access."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawAudit(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawAudit sub-model for audit."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawCreateDir(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawCreateDir sub-model for dir."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawCreateFile(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawCreateFile sub-model for file."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawCreateOther(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawCreateOther sub-model for other."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawCreateSymlink(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawCreateSymlink sub-model for symlink."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawCreate(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawCreate sub-model for create."""

    dir: OntapVolumeStatisticsCifsOpsRawCreateDir = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawCreateDir
    )
    file: OntapVolumeStatisticsCifsOpsRawCreateFile = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawCreateFile
    )
    other: OntapVolumeStatisticsCifsOpsRawCreateOther = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawCreateOther
    )
    symlink: OntapVolumeStatisticsCifsOpsRawCreateSymlink = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawCreateSymlink
    )


class OntapVolumeStatisticsCifsOpsRawGetattr(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawGetattr sub-model for getattr."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawLink(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawLink sub-model for link."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawLock(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawLock sub-model for lock."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawLookup(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawLookup sub-model for lookup."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawOpen(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawOpen sub-model for open."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawRead(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawRead sub-model for read."""

    count: int = 0
    total_time: int = 0
    volume_protocol_latency_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_latency_histogram_labels: list[str] = Field(default_factory=list)
    volume_protocol_size_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_size_histogram_labels: list[str] = Field(default_factory=list)


class OntapVolumeStatisticsCifsOpsRawReaddir(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawReaddir sub-model for readdir."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawReadlink(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawReadlink sub-model for readlink."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawRename(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawRename sub-model for rename."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawSetattr(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawSetattr sub-model for setattr."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawUnlink(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawUnlink sub-model for unlink."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawWatch(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawWatch sub-model for watch."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsCifsOpsRawWrite(OntapModel):
    """OntapVolumeStatisticsCifsOpsRawWrite sub-model for write."""

    count: int = 0
    total_time: int = 0
    volume_protocol_latency_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_latency_histogram_labels: list[str] = Field(default_factory=list)
    volume_protocol_size_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_size_histogram_labels: list[str] = Field(default_factory=list)


class OntapVolumeStatisticsCifsOpsRaw(OntapModel):
    """OntapVolumeStatisticsCifsOpsRaw sub-model for cifs_ops_raw."""

    access: OntapVolumeStatisticsCifsOpsRawAccess = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawAccess
    )
    audit: OntapVolumeStatisticsCifsOpsRawAudit = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawAudit
    )
    create: OntapVolumeStatisticsCifsOpsRawCreate = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawCreate
    )
    getattr: OntapVolumeStatisticsCifsOpsRawGetattr = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawGetattr
    )
    link: OntapVolumeStatisticsCifsOpsRawLink = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawLink
    )
    lock: OntapVolumeStatisticsCifsOpsRawLock = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawLock
    )
    lookup: OntapVolumeStatisticsCifsOpsRawLookup = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawLookup
    )
    open: OntapVolumeStatisticsCifsOpsRawOpen = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawOpen
    )
    read: OntapVolumeStatisticsCifsOpsRawRead = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawRead
    )
    readdir: OntapVolumeStatisticsCifsOpsRawReaddir = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawReaddir
    )
    readlink: OntapVolumeStatisticsCifsOpsRawReadlink = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawReadlink
    )
    rename: OntapVolumeStatisticsCifsOpsRawRename = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawRename
    )
    setattr: OntapVolumeStatisticsCifsOpsRawSetattr = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawSetattr
    )
    unlink: OntapVolumeStatisticsCifsOpsRawUnlink = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawUnlink
    )
    watch: OntapVolumeStatisticsCifsOpsRawWatch = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawWatch
    )
    write: OntapVolumeStatisticsCifsOpsRawWrite = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRawWrite
    )


class OntapVolumeStatisticsCloudIopsRaw(OntapModel):
    """OntapVolumeStatisticsCloudIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeStatisticsCloudLatencyRaw(OntapModel):
    """OntapVolumeStatisticsCloudLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeStatisticsCloud(OntapModel):
    """OntapVolumeStatisticsCloud sub-model for cloud."""

    iops_raw: OntapVolumeStatisticsCloudIopsRaw = Field(
        default_factory=OntapVolumeStatisticsCloudIopsRaw
    )
    latency_raw: OntapVolumeStatisticsCloudLatencyRaw = Field(
        default_factory=OntapVolumeStatisticsCloudLatencyRaw
    )
    status: str = ""
    timestamp: str = ""


class OntapVolumeStatisticsFlexcacheRaw(OntapModel):
    """OntapVolumeStatisticsFlexcacheRaw sub-model for flexcache_raw."""

    cache_miss_blocks: int = 0
    client_requested_blocks: int = 0
    status: str = ""
    timestamp: str = ""


class OntapVolumeStatisticsIopsRaw(OntapModel):
    """OntapVolumeStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeStatisticsLatencyRaw(OntapModel):
    """OntapVolumeStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeStatisticsNfsOpsRawAccess(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawAccess sub-model for access."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawAudit(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawAudit sub-model for audit."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawCreateDir(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawCreateDir sub-model for dir."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawCreateFile(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawCreateFile sub-model for file."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawCreateOther(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawCreateOther sub-model for other."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawCreateSymlink(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawCreateSymlink sub-model for symlink."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawCreate(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawCreate sub-model for create."""

    dir: OntapVolumeStatisticsNfsOpsRawCreateDir = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawCreateDir
    )
    file: OntapVolumeStatisticsNfsOpsRawCreateFile = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawCreateFile
    )
    other: OntapVolumeStatisticsNfsOpsRawCreateOther = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawCreateOther
    )
    symlink: OntapVolumeStatisticsNfsOpsRawCreateSymlink = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawCreateSymlink
    )


class OntapVolumeStatisticsNfsOpsRawGetattr(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawGetattr sub-model for getattr."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawLink(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawLink sub-model for link."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawLock(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawLock sub-model for lock."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawLookup(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawLookup sub-model for lookup."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawOpen(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawOpen sub-model for open."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawRead(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawRead sub-model for read."""

    count: int = 0
    total_time: int = 0
    volume_protocol_latency_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_latency_histogram_labels: list[str] = Field(default_factory=list)
    volume_protocol_size_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_size_histogram_labels: list[str] = Field(default_factory=list)


class OntapVolumeStatisticsNfsOpsRawReaddir(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawReaddir sub-model for readdir."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawReadlink(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawReadlink sub-model for readlink."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawRename(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawRename sub-model for rename."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawSetattr(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawSetattr sub-model for setattr."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawUnlink(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawUnlink sub-model for unlink."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawWatch(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawWatch sub-model for watch."""

    count: int = 0
    total_time: int = 0


class OntapVolumeStatisticsNfsOpsRawWrite(OntapModel):
    """OntapVolumeStatisticsNfsOpsRawWrite sub-model for write."""

    count: int = 0
    total_time: int = 0
    volume_protocol_latency_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_latency_histogram_labels: list[str] = Field(default_factory=list)
    volume_protocol_size_histogram_counts: list[int] = Field(default_factory=list)
    volume_protocol_size_histogram_labels: list[str] = Field(default_factory=list)


class OntapVolumeStatisticsNfsOpsRaw(OntapModel):
    """OntapVolumeStatisticsNfsOpsRaw sub-model for nfs_ops_raw."""

    access: OntapVolumeStatisticsNfsOpsRawAccess = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawAccess
    )
    audit: OntapVolumeStatisticsNfsOpsRawAudit = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawAudit
    )
    create: OntapVolumeStatisticsNfsOpsRawCreate = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawCreate
    )
    getattr: OntapVolumeStatisticsNfsOpsRawGetattr = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawGetattr
    )
    link: OntapVolumeStatisticsNfsOpsRawLink = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawLink
    )
    lock: OntapVolumeStatisticsNfsOpsRawLock = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawLock
    )
    lookup: OntapVolumeStatisticsNfsOpsRawLookup = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawLookup
    )
    open: OntapVolumeStatisticsNfsOpsRawOpen = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawOpen
    )
    read: OntapVolumeStatisticsNfsOpsRawRead = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawRead
    )
    readdir: OntapVolumeStatisticsNfsOpsRawReaddir = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawReaddir
    )
    readlink: OntapVolumeStatisticsNfsOpsRawReadlink = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawReadlink
    )
    rename: OntapVolumeStatisticsNfsOpsRawRename = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawRename
    )
    setattr: OntapVolumeStatisticsNfsOpsRawSetattr = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawSetattr
    )
    unlink: OntapVolumeStatisticsNfsOpsRawUnlink = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawUnlink
    )
    watch: OntapVolumeStatisticsNfsOpsRawWatch = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawWatch
    )
    write: OntapVolumeStatisticsNfsOpsRawWrite = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRawWrite
    )


class OntapVolumeStatisticsThroughputRaw(OntapModel):
    """OntapVolumeStatisticsThroughputRaw sub-model for throughput_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeStatistics(OntapModel):
    """OntapVolumeStatistics sub-model for statistics."""

    cifs_ops_raw: OntapVolumeStatisticsCifsOpsRaw = Field(
        default_factory=OntapVolumeStatisticsCifsOpsRaw
    )
    cloud: OntapVolumeStatisticsCloud = Field(default_factory=OntapVolumeStatisticsCloud)
    flexcache_raw: OntapVolumeStatisticsFlexcacheRaw = Field(
        default_factory=OntapVolumeStatisticsFlexcacheRaw
    )
    iops_raw: OntapVolumeStatisticsIopsRaw = Field(default_factory=OntapVolumeStatisticsIopsRaw)
    latency_raw: OntapVolumeStatisticsLatencyRaw = Field(
        default_factory=OntapVolumeStatisticsLatencyRaw
    )
    nfs_ops_raw: OntapVolumeStatisticsNfsOpsRaw = Field(
        default_factory=OntapVolumeStatisticsNfsOpsRaw
    )
    status: str = ""
    throughput_raw: OntapVolumeStatisticsThroughputRaw = Field(
        default_factory=OntapVolumeStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapVolumeSvm(OntapModel):
    """OntapVolumeSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVolumeTiering(OntapModel):
    """OntapVolumeTiering sub-model for tiering."""

    min_cooling_days: int = 0
    object_tags: list[str] = Field(default_factory=list)
    policy: str = ""
    supported: bool = False


class OntapVolume(OntapModel):
    """OntapVolume information."""

    access_time_enabled: bool = False
    activity_tracking: OntapVolumeActivityTracking = Field(
        default_factory=OntapVolumeActivityTracking
    )
    aggregates: list[OntapVolumeAggregate] = Field(default_factory=list)
    aggressive_readahead_mode: str = ""
    analytics: OntapVolumeAnalytics = Field(default_factory=OntapVolumeAnalytics)
    anti_ransomware: OntapVolumeAntiRansomware = Field(default_factory=OntapVolumeAntiRansomware)
    application: OntapVolumeApplication = Field(default_factory=OntapVolumeApplication)
    asynchronous_directory_delete: OntapVolumeAsynchronousDirectoryDelete = Field(
        default_factory=OntapVolumeAsynchronousDirectoryDelete
    )
    autosize: OntapVolumeAutosize = Field(default_factory=OntapVolumeAutosize)
    clone: OntapVolumeClone = Field(default_factory=OntapVolumeClone)
    cloud_retrieval_policy: str = ""
    cloud_write_enabled: bool = False
    comment: str = ""
    consistency_group: OntapVolumeConsistencyGroup = Field(
        default_factory=OntapVolumeConsistencyGroup
    )
    constituents: list[OntapVolumeConstituent] = Field(default_factory=list)
    constituents_per_aggregate: int = 0
    convert_unicode: bool = False
    create_time: str = ""
    efficiency: OntapVolumeEfficiency = Field(default_factory=OntapVolumeEfficiency)
    encryption: OntapVolumeEncryption = Field(default_factory=OntapVolumeEncryption)
    error_state: OntapVolumeErrorState = Field(default_factory=OntapVolumeErrorState)
    files: OntapVolumeFiles = Field(default_factory=OntapVolumeFiles)
    flash_pool: OntapVolumeFlashPool = Field(default_factory=OntapVolumeFlashPool)
    flexcache_endpoint_type: str = ""
    flexgroup: OntapVolumeFlexgroup = Field(default_factory=OntapVolumeFlexgroup)
    granular_data: bool = False
    granular_data_mode: str = ""
    guarantee: OntapVolumeGuarantee = Field(default_factory=OntapVolumeGuarantee)
    is_object_store: bool = False
    is_svm_root: bool = False
    language: str = ""
    max_dir_size: int = 0
    metric: OntapVolumeMetric = Field(default_factory=OntapVolumeMetric)
    movement: OntapVolumeMovement = Field(default_factory=OntapVolumeMovement)
    msid: int = 0
    name: str = ""
    nas: OntapVolumeNas = Field(default_factory=OntapVolumeNas)
    optimize_aggregates: bool = False
    qos: OntapVolumeQos = Field(default_factory=OntapVolumeQos)
    queue_for_encryption: bool = False
    quota: OntapVolumeQuota = Field(default_factory=OntapVolumeQuota)
    rebalancing: OntapVolumeRebalancing = Field(default_factory=OntapVolumeRebalancing)
    scheduled_snapshot_naming_scheme: str = ""
    size: int = 0
    snaplock: OntapVolumeSnaplock = Field(default_factory=OntapVolumeSnaplock)
    snapmirror: OntapVolumeSnapmirror = Field(default_factory=OntapVolumeSnapmirror)
    snapshot_count: int = 0
    snapshot_directory_access_enabled: bool = False
    snapshot_locking_enabled: bool = False
    snapshot_policy: OntapVolumeSnapshotPolicy = Field(default_factory=OntapVolumeSnapshotPolicy)
    space: OntapVolumeSpace = Field(default_factory=OntapVolumeSpace)
    state: str = ""
    statistics: OntapVolumeStatistics = Field(default_factory=OntapVolumeStatistics)
    status: list[str] = Field(default_factory=list)
    style: str = ""
    svm: OntapVolumeSvm = Field(default_factory=OntapVolumeSvm)
    tiering: OntapVolumeTiering = Field(default_factory=OntapVolumeTiering)
    type_: str = ""
    use_mirrored_aggregates: bool = False
    uuid: str = ""
    validate_only: bool = False
