# ruff: noqa: E501
"""OntapVolume information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVolumeAggregate(OntapModel):
    """OntapVolumeAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapVolumeAttackReport(OntapModel):
    """OntapVolumeAttackReport sub-model for attack_reports."""

    time: str = ""


class OntapVolumeSuspectFile(OntapModel):
    """OntapVolumeSuspectFile sub-model for suspect_files."""

    count: int = 0
    entropy: str = ""
    format: str = ""


class OntapVolumeNewlyObservedFileExtension(OntapModel):
    """OntapVolumeNewlyObservedFileExtension sub-model for newly_observed_file_extensions."""

    count: int = 0
    name: str = ""


class OntapVolumeNewlyObservedFileExtension2(OntapModel):
    """OntapVolumeNewlyObservedFileExtension2 sub-model for newly_observed_file_extensions."""

    count: int = 0
    name: str = ""


class OntapVolumeConstituent(OntapModel):
    """OntapVolumeConstituent sub-model for constituents."""

    aggregates_name: str = ""
    aggregates_uuid: str = ""
    movement_cutover_window: int = 0
    movement_destination_aggregate_name: str = ""
    movement_destination_aggregate_uuid: str = ""
    movement_percent_complete: int = 0
    movement_state: str = ""
    movement_tiering_policy: str = ""
    name: str = ""
    space_afs_total: int = 0
    space_available: int = 0
    space_available_percent: int = 0
    space_block_storage_inactive_user_data: int = 0
    space_capacity_tier_footprint: int = 0
    space_footprint: int = 0
    space_large_size_enabled: bool = False
    space_local_tier_footprint: int = 0
    space_logical_space_available: int = 0
    space_logical_space_enforcement: bool = False
    space_logical_space_reporting: bool = False
    space_logical_space_used_by_afs: int = 0
    space_max_size: str = ""
    space_metadata: int = 0
    space_over_provisioned: int = 0
    space_performance_tier_footprint: int = 0
    space_size: int = 0
    space_snapshot_autodelete_enabled: bool = False
    space_snapshot_reserve_percent: int = 0
    space_snapshot_used: int = 0
    space_total_footprint: int = 0
    space_total_metadata: int = 0
    space_total_metadata_footprint: int = 0
    space_used: int = 0
    space_used_by_afs: int = 0
    space_used_percent: int = 0


class OntapVolumeNotice(OntapModel):
    """OntapVolumeNotice sub-model for notices."""

    arguments: list[dict[str, Any]] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapVolume(OntapModel):
    """OntapVolume information."""

    access_time_enabled: bool = False
    activity_tracking_state: str = ""
    activity_tracking_supported: bool = False
    activity_tracking_unsupported_reason_code: str = ""
    activity_tracking_unsupported_reason_message: str = ""
    aggregates: list[OntapVolumeAggregate] = Field(default_factory=list)
    aggressive_readahead_mode: str = ""
    analytics_files_scanned: int = 0
    analytics_initialization_state: str = ""
    analytics_scan_progress: int = 0
    analytics_scan_throttle_reason_arguments: list[str] = Field(default_factory=list)
    analytics_scan_throttle_reason_code: str = ""
    analytics_scan_throttle_reason_message: str = ""
    analytics_state: str = ""
    analytics_supported: bool = False
    analytics_total_files: int = 0
    analytics_unsupported_reason_code: str = ""
    analytics_unsupported_reason_message: str = ""
    anti_ransomware_attack_detection_parameters_based_on_file_create_op_rate: bool = False
    anti_ransomware_attack_detection_parameters_based_on_file_delete_op_rate: bool = False
    anti_ransomware_attack_detection_parameters_based_on_file_rename_op_rate: bool = False
    anti_ransomware_attack_detection_parameters_based_on_high_entropy_data_rate: bool = False
    anti_ransomware_attack_detection_parameters_based_on_never_seen_before_file_extension: bool = (
        False
    )
    anti_ransomware_attack_detection_parameters_file_create_op_rate_surge_notify_percent: int = 0
    anti_ransomware_attack_detection_parameters_file_delete_op_rate_surge_notify_percent: int = 0
    anti_ransomware_attack_detection_parameters_file_rename_op_rate_surge_notify_percent: int = 0
    anti_ransomware_attack_detection_parameters_high_entropy_data_surge_notify_percent: int = 0
    anti_ransomware_attack_detection_parameters_never_seen_before_file_extension_count_notify_threshold: int = 0
    anti_ransomware_attack_detection_parameters_never_seen_before_file_extension_duration_in_hours: int = 0
    anti_ransomware_attack_detection_parameters_relaxing_popular_file_extensions: bool = False
    anti_ransomware_attack_probability: str = ""
    anti_ransomware_attack_reports: list[OntapVolumeAttackReport] = Field(default_factory=list)
    anti_ransomware_dry_run_start_time: str = ""
    anti_ransomware_event_log_is_enabled_on_new_file_extension_seen: bool = False
    anti_ransomware_event_log_is_enabled_on_snapshot_copy_creation: bool = False
    anti_ransomware_space_snapshot_count: int = 0
    anti_ransomware_space_used: int = 0
    anti_ransomware_space_used_by_logs: int = 0
    anti_ransomware_space_used_by_snapshots: int = 0
    anti_ransomware_state: str = ""
    anti_ransomware_surge_as_normal: bool = False
    anti_ransomware_surge_usage_file_create_peak_rate_per_minute: int = 0
    anti_ransomware_surge_usage_file_delete_peak_rate_per_minute: int = 0
    anti_ransomware_surge_usage_file_rename_peak_rate_per_minute: int = 0
    anti_ransomware_surge_usage_high_entropy_data_write_peak_percent: int = 0
    anti_ransomware_surge_usage_high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    anti_ransomware_surge_usage_time: str = ""
    anti_ransomware_suspect_files: list[OntapVolumeSuspectFile] = Field(default_factory=list)
    anti_ransomware_typical_usage_file_create_peak_rate_per_minute: int = 0
    anti_ransomware_typical_usage_file_delete_peak_rate_per_minute: int = 0
    anti_ransomware_typical_usage_file_rename_peak_rate_per_minute: int = 0
    anti_ransomware_typical_usage_high_entropy_data_write_peak_percent: int = 0
    anti_ransomware_typical_usage_high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    anti_ransomware_update_baseline_from_surge: bool = False
    anti_ransomware_workload_file_extension_types_count: int = 0
    anti_ransomware_workload_file_extensions_observed: list[str] = Field(default_factory=list)
    anti_ransomware_workload_historical_statistics_file_create_peak_rate_per_minute: int = 0
    anti_ransomware_workload_historical_statistics_file_delete_peak_rate_per_minute: int = 0
    anti_ransomware_workload_historical_statistics_file_rename_peak_rate_per_minute: int = 0
    anti_ransomware_workload_historical_statistics_high_entropy_data_write_peak_percent: int = 0
    anti_ransomware_workload_historical_statistics_high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    anti_ransomware_workload_newly_observed_file_extensions: list[
        OntapVolumeNewlyObservedFileExtension
    ] = Field(default_factory=list)
    anti_ransomware_workload_surge_statistics_file_create_peak_rate_per_minute: int = 0
    anti_ransomware_workload_surge_statistics_file_delete_peak_rate_per_minute: int = 0
    anti_ransomware_workload_surge_statistics_file_rename_peak_rate_per_minute: int = 0
    anti_ransomware_workload_surge_statistics_high_entropy_data_write_peak_percent: int = 0
    anti_ransomware_workload_surge_statistics_high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    anti_ransomware_workload_surge_statistics_time: str = ""
    anti_ransomware_workload_surge_usage_file_create_peak_rate_per_minute: int = 0
    anti_ransomware_workload_surge_usage_file_delete_peak_rate_per_minute: int = 0
    anti_ransomware_workload_surge_usage_file_rename_peak_rate_per_minute: int = 0
    anti_ransomware_workload_surge_usage_high_entropy_data_write_peak_percent: int = 0
    anti_ransomware_workload_surge_usage_high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    anti_ransomware_workload_surge_usage_newly_observed_file_extensions: list[
        OntapVolumeNewlyObservedFileExtension2
    ] = Field(default_factory=list)
    anti_ransomware_workload_surge_usage_time: str = ""
    anti_ransomware_workload_typical_usage_file_create_peak_rate_per_minute: int = 0
    anti_ransomware_workload_typical_usage_file_delete_peak_rate_per_minute: int = 0
    anti_ransomware_workload_typical_usage_file_rename_peak_rate_per_minute: int = 0
    anti_ransomware_workload_typical_usage_high_entropy_data_write_peak_percent: int = 0
    anti_ransomware_workload_typical_usage_high_entropy_data_write_peak_rate_kb_per_minute: int = 0
    application_name: str = ""
    application_uuid: str = ""
    asynchronous_directory_delete_enabled: bool = False
    asynchronous_directory_delete_trash_bin: str = ""
    autosize_grow_threshold: int = 0
    autosize_maximum: int = 0
    autosize_minimum: int = 0
    autosize_mode: str = ""
    autosize_shrink_threshold: int = 0
    clone_has_flexclone: bool = False
    clone_inherited_physical_used: int = 0
    clone_inherited_savings: int = 0
    clone_is_flexclone: bool = False
    clone_parent_snapshot_name: str = ""
    clone_parent_snapshot_uuid: str = ""
    clone_parent_svm_name: str = ""
    clone_parent_svm_uuid: str = ""
    clone_parent_volume_name: str = ""
    clone_parent_volume_uuid: str = ""
    clone_split_complete_percent: int = 0
    clone_split_estimate: int = 0
    clone_split_initiated: bool = False
    cloud_retrieval_policy: str = ""
    cloud_write_enabled: bool = False
    comment: str = ""
    consistency_group_name: str = ""
    consistency_group_uuid: str = ""
    constituents: list[OntapVolumeConstituent] = Field(default_factory=list)
    constituents_per_aggregate: int = 0
    convert_unicode: bool = False
    create_time: str = ""
    efficiency_application_io_size: str = ""
    efficiency_auto_state: str = ""
    efficiency_compaction: str = ""
    efficiency_compression: str = ""
    efficiency_compression_type: str = ""
    efficiency_cross_volume_dedupe: str = ""
    efficiency_dedupe: str = ""
    efficiency_has_savings: bool = False
    efficiency_idcs_scanner_enabled: bool = False
    efficiency_idcs_scanner_inactive_days: int = 0
    efficiency_idcs_scanner_mode: str = ""
    efficiency_idcs_scanner_operation_state: str = ""
    efficiency_idcs_scanner_status: str = ""
    efficiency_idcs_scanner_threshold_inactive_time: str = ""
    efficiency_last_op_begin: str = ""
    efficiency_last_op_end: str = ""
    efficiency_last_op_err: str = ""
    efficiency_last_op_size: int = 0
    efficiency_last_op_state: str = ""
    efficiency_logging_enabled: bool = False
    efficiency_op_state: str = ""
    efficiency_policy_name: str = ""
    efficiency_progress: str = ""
    efficiency_scanner_compression: bool = False
    efficiency_scanner_dedupe: bool = False
    efficiency_scanner_scan_old_data: bool = False
    efficiency_scanner_state: str = ""
    efficiency_schedule: str = ""
    efficiency_space_savings_compression: int = 0
    efficiency_space_savings_compression_percent: int = 0
    efficiency_space_savings_dedupe: int = 0
    efficiency_space_savings_dedupe_percent: int = 0
    efficiency_space_savings_dedupe_sharing: int = 0
    efficiency_space_savings_total: int = 0
    efficiency_space_savings_total_percent: int = 0
    efficiency_state: str = ""
    efficiency_storage_efficiency_mode: str = ""
    efficiency_type: str = ""
    efficiency_volume_path: str = ""
    encryption_action: str = ""
    encryption_enabled: bool = False
    encryption_key_create_time: str = ""
    encryption_key_id: str = ""
    encryption_key_manager_attribute: str = ""
    encryption_rekey: bool = False
    encryption_state: str = ""
    encryption_status_code: str = ""
    encryption_status_message: str = ""
    encryption_type: str = ""
    error_state_has_bad_blocks: bool = False
    error_state_is_inconsistent: bool = False
    files_maximum: int = 0
    files_used: int = 0
    flash_pool_cache_eligibility: str = ""
    flash_pool_cache_retention_priority: str = ""
    flash_pool_caching_policy: str = ""
    flexcache_endpoint_type: str = ""
    flexgroup_name: str = ""
    flexgroup_uuid: str = ""
    granular_data: bool = False
    granular_data_mode: str = ""
    guarantee_honored: bool = False
    guarantee_type: str = ""
    is_object_store: bool = False
    is_svm_root: bool = False
    language: str = ""
    max_dir_size: int = 0
    metric_cloud_duration: str = ""
    metric_cloud_iops_other: int = 0
    metric_cloud_iops_read: int = 0
    metric_cloud_iops_total: int = 0
    metric_cloud_iops_write: int = 0
    metric_cloud_latency_other: int = 0
    metric_cloud_latency_read: int = 0
    metric_cloud_latency_total: int = 0
    metric_cloud_latency_write: int = 0
    metric_cloud_status: str = ""
    metric_cloud_timestamp: str = ""
    metric_duration: str = ""
    metric_flexcache_bandwidth_savings: int = 0
    metric_flexcache_cache_miss_percent: int = 0
    metric_flexcache_duration: str = ""
    metric_flexcache_status: str = ""
    metric_flexcache_timestamp: str = ""
    metric_iops_other: int = 0
    metric_iops_read: int = 0
    metric_iops_total: int = 0
    metric_iops_write: int = 0
    metric_latency_other: int = 0
    metric_latency_read: int = 0
    metric_latency_total: int = 0
    metric_latency_write: int = 0
    metric_status: str = ""
    metric_throughput_other: int = 0
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    movement_capacity_tier_optimized: bool = False
    movement_cutover_window: int = 0
    movement_destination_aggregate_name: str = ""
    movement_destination_aggregate_uuid: str = ""
    movement_percent_complete: int = 0
    movement_start_time: str = ""
    movement_state: str = ""
    movement_tiering_policy: str = ""
    msid: int = 0
    name: str = ""
    nas_export_policy_id: int = 0
    nas_export_policy_name: str = ""
    nas_gid: int = 0
    nas_junction_parent_name: str = ""
    nas_junction_parent_uuid: str = ""
    nas_path: str = ""
    nas_security_style: str = ""
    nas_uid: int = 0
    nas_unix_permissions: int = 0
    optimize_aggregates: bool = False
    qos_policy_max_throughput_iops: int = 0
    qos_policy_max_throughput_mbps: int = 0
    qos_policy_min_throughput_iops: int = 0
    qos_policy_min_throughput_mbps: int = 0
    qos_policy_name: str = ""
    qos_policy_uuid: str = ""
    queue_for_encryption: bool = False
    quota_enabled: bool = False
    quota_state: str = ""
    rebalancing_data_moved: int = 0
    rebalancing_engine_movement_file_moves_started: int = 0
    rebalancing_engine_movement_last_error_code: int = 0
    rebalancing_engine_movement_last_error_destination: int = 0
    rebalancing_engine_movement_last_error_file_id: int = 0
    rebalancing_engine_movement_last_error_time: str = ""
    rebalancing_engine_movement_most_recent_start_time: str = ""
    rebalancing_engine_scanner_blocks_scanned: int = 0
    rebalancing_engine_scanner_blocks_skipped_efficiency_blocks: int = 0
    rebalancing_engine_scanner_blocks_skipped_efficiency_percent: int = 0
    rebalancing_engine_scanner_blocks_skipped_fast_truncate: int = 0
    rebalancing_engine_scanner_blocks_skipped_footprint_invalid: int = 0
    rebalancing_engine_scanner_blocks_skipped_in_snapshot: int = 0
    rebalancing_engine_scanner_blocks_skipped_incompatible: int = 0
    rebalancing_engine_scanner_blocks_skipped_metadata: int = 0
    rebalancing_engine_scanner_blocks_skipped_on_demand_destination: int = 0
    rebalancing_engine_scanner_blocks_skipped_other: int = 0
    rebalancing_engine_scanner_blocks_skipped_remote_cache: int = 0
    rebalancing_engine_scanner_blocks_skipped_too_large: int = 0
    rebalancing_engine_scanner_blocks_skipped_too_small: int = 0
    rebalancing_engine_scanner_blocks_skipped_write_fenced: int = 0
    rebalancing_engine_scanner_files_scanned: int = 0
    rebalancing_engine_scanner_files_skipped_efficiency_blocks: int = 0
    rebalancing_engine_scanner_files_skipped_efficiency_percent: int = 0
    rebalancing_engine_scanner_files_skipped_fast_truncate: int = 0
    rebalancing_engine_scanner_files_skipped_footprint_invalid: int = 0
    rebalancing_engine_scanner_files_skipped_in_snapshot: int = 0
    rebalancing_engine_scanner_files_skipped_incompatible: int = 0
    rebalancing_engine_scanner_files_skipped_metadata: int = 0
    rebalancing_engine_scanner_files_skipped_on_demand_destination: int = 0
    rebalancing_engine_scanner_files_skipped_other: int = 0
    rebalancing_engine_scanner_files_skipped_remote_cache: int = 0
    rebalancing_engine_scanner_files_skipped_too_large: int = 0
    rebalancing_engine_scanner_files_skipped_too_small: int = 0
    rebalancing_engine_scanner_files_skipped_write_fenced: int = 0
    rebalancing_exclude_snapshots: bool = False
    rebalancing_imbalance_percent: int = 0
    rebalancing_imbalance_size: int = 0
    rebalancing_max_constituent_imbalance_percent: int = 0
    rebalancing_max_file_moves: int = 0
    rebalancing_max_runtime: str = ""
    rebalancing_max_threshold: int = 0
    rebalancing_min_file_size: int = 0
    rebalancing_min_threshold: int = 0
    rebalancing_notices: list[OntapVolumeNotice] = Field(default_factory=list)
    rebalancing_runtime: str = ""
    rebalancing_start_time: str = ""
    rebalancing_state: str = ""
    rebalancing_stop_time: str = ""
    rebalancing_target_used: int = 0
    rebalancing_used_for_imbalance: int = 0
    scheduled_snapshot_naming_scheme: str = ""
    size: int = 0
    snaplock_append_mode_enabled: bool = False
    snaplock_autocommit_period: str = ""
    snaplock_compliance_clock_time: str = ""
    snaplock_expiry_time: str = ""
    snaplock_is_audit_log: bool = False
    snaplock_litigation_count: int = 0
    snaplock_privileged_delete: str = ""
    snaplock_retention_default: str = ""
    snaplock_retention_maximum: str = ""
    snaplock_retention_minimum: str = ""
    snaplock_type: str = ""
    snaplock_unspecified_retention_file_count: int = 0
    snapmirror_destinations_is_cloud: bool = False
    snapmirror_destinations_is_ontap: bool = False
    snapmirror_is_protected: bool = False
    snapshot_count: int = 0
    snapshot_directory_access_enabled: bool = False
    snapshot_locking_enabled: bool = False
    snapshot_policy_name: str = ""
    snapshot_policy_uuid: str = ""
    space_afs_total: int = 0
    space_auto_adaptive_compression_footprint_data_reduction: int = 0
    space_available: int = 0
    space_available_percent: int = 0
    space_block_storage_inactive_user_data: int = 0
    space_block_storage_inactive_user_data_percent: int = 0
    space_capacity_tier_footprint: int = 0
    space_capacity_tier_footprint_data_reduction: int = 0
    space_compaction_footprint_data_reduction: int = 0
    space_cross_volume_dedupe_metafiles_footprint: int = 0
    space_cross_volume_dedupe_metafiles_temporary_footprint: int = 0
    space_dedupe_metafiles_footprint: int = 0
    space_dedupe_metafiles_temporary_footprint: int = 0
    space_delayed_free_footprint: int = 0
    space_effective_total_footprint: int = 0
    space_expected_available: int = 0
    space_file_operation_metadata: int = 0
    space_filesystem_size: int = 0
    space_filesystem_size_fixed: bool = False
    space_footprint: int = 0
    space_fractional_reserve: int = 0
    space_full_threshold_percent: int = 0
    space_is_used_stale: bool = False
    space_large_size_enabled: bool = False
    space_local_tier_footprint: int = 0
    space_logical_space_available: int = 0
    space_logical_space_enforcement: bool = False
    space_logical_space_reporting: bool = False
    space_logical_space_used: int = 0
    space_logical_space_used_by_afs: int = 0
    space_logical_space_used_by_snapshots: int = 0
    space_logical_space_used_percent: int = 0
    space_max_size: str = ""
    space_metadata: int = 0
    space_nearly_full_threshold_percent: int = 0
    space_over_provisioned: int = 0
    space_overwrite_reserve: int = 0
    space_overwrite_reserve_used: int = 0
    space_percent_used: int = 0
    space_performance_tier_footprint: int = 0
    space_physical_used: int = 0
    space_physical_used_percent: int = 0
    space_size: int = 0
    space_size_available_for_snapshots: int = 0
    space_snapmirror_destination_footprint: int = 0
    space_snapshot_autodelete_commitment: str = ""
    space_snapshot_autodelete_defer_delete: str = ""
    space_snapshot_autodelete_delete_order: str = ""
    space_snapshot_autodelete_enabled: bool = False
    space_snapshot_autodelete_prefix: str = ""
    space_snapshot_autodelete_target_free_space: int = 0
    space_snapshot_autodelete_trigger: str = ""
    space_snapshot_reserve_available: int = 0
    space_snapshot_reserve_percent: int = 0
    space_snapshot_reserve_size: int = 0
    space_snapshot_space_used_percent: int = 0
    space_snapshot_used: int = 0
    space_snapshot_reserve_unusable: int = 0
    space_snapshot_spill: int = 0
    space_total_footprint: int = 0
    space_total_metadata: int = 0
    space_total_metadata_footprint: int = 0
    space_used: int = 0
    space_used_by_afs: int = 0
    space_user_data: int = 0
    space_volume_guarantee_footprint: int = 0
    state: str = ""
    statistics_cifs_ops_raw_access_count: int = 0
    statistics_cifs_ops_raw_access_total_time: int = 0
    statistics_cifs_ops_raw_audit_count: int = 0
    statistics_cifs_ops_raw_audit_total_time: int = 0
    statistics_cifs_ops_raw_create_dir_count: int = 0
    statistics_cifs_ops_raw_create_dir_total_time: int = 0
    statistics_cifs_ops_raw_create_file_count: int = 0
    statistics_cifs_ops_raw_create_file_total_time: int = 0
    statistics_cifs_ops_raw_create_other_count: int = 0
    statistics_cifs_ops_raw_create_other_total_time: int = 0
    statistics_cifs_ops_raw_create_symlink_count: int = 0
    statistics_cifs_ops_raw_create_symlink_total_time: int = 0
    statistics_cifs_ops_raw_getattr_count: int = 0
    statistics_cifs_ops_raw_getattr_total_time: int = 0
    statistics_cifs_ops_raw_link_count: int = 0
    statistics_cifs_ops_raw_link_total_time: int = 0
    statistics_cifs_ops_raw_lock_count: int = 0
    statistics_cifs_ops_raw_lock_total_time: int = 0
    statistics_cifs_ops_raw_lookup_count: int = 0
    statistics_cifs_ops_raw_lookup_total_time: int = 0
    statistics_cifs_ops_raw_open_count: int = 0
    statistics_cifs_ops_raw_open_total_time: int = 0
    statistics_cifs_ops_raw_read_count: int = 0
    statistics_cifs_ops_raw_read_total_time: int = 0
    statistics_cifs_ops_raw_read_volume_protocol_latency_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_read_volume_protocol_latency_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_read_volume_protocol_size_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_read_volume_protocol_size_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_readdir_count: int = 0
    statistics_cifs_ops_raw_readdir_total_time: int = 0
    statistics_cifs_ops_raw_readlink_count: int = 0
    statistics_cifs_ops_raw_readlink_total_time: int = 0
    statistics_cifs_ops_raw_rename_count: int = 0
    statistics_cifs_ops_raw_rename_total_time: int = 0
    statistics_cifs_ops_raw_setattr_count: int = 0
    statistics_cifs_ops_raw_setattr_total_time: int = 0
    statistics_cifs_ops_raw_unlink_count: int = 0
    statistics_cifs_ops_raw_unlink_total_time: int = 0
    statistics_cifs_ops_raw_watch_count: int = 0
    statistics_cifs_ops_raw_watch_total_time: int = 0
    statistics_cifs_ops_raw_write_count: int = 0
    statistics_cifs_ops_raw_write_total_time: int = 0
    statistics_cifs_ops_raw_write_volume_protocol_latency_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_write_volume_protocol_latency_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_write_volume_protocol_size_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_cifs_ops_raw_write_volume_protocol_size_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_cloud_iops_raw_other: int = 0
    statistics_cloud_iops_raw_read: int = 0
    statistics_cloud_iops_raw_total: int = 0
    statistics_cloud_iops_raw_write: int = 0
    statistics_cloud_latency_raw_other: int = 0
    statistics_cloud_latency_raw_read: int = 0
    statistics_cloud_latency_raw_total: int = 0
    statistics_cloud_latency_raw_write: int = 0
    statistics_cloud_status: str = ""
    statistics_cloud_timestamp: str = ""
    statistics_flexcache_raw_cache_miss_blocks: int = 0
    statistics_flexcache_raw_client_requested_blocks: int = 0
    statistics_flexcache_raw_status: str = ""
    statistics_flexcache_raw_timestamp: str = ""
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_nfs_ops_raw_access_count: int = 0
    statistics_nfs_ops_raw_access_total_time: int = 0
    statistics_nfs_ops_raw_audit_count: int = 0
    statistics_nfs_ops_raw_audit_total_time: int = 0
    statistics_nfs_ops_raw_create_dir_count: int = 0
    statistics_nfs_ops_raw_create_dir_total_time: int = 0
    statistics_nfs_ops_raw_create_file_count: int = 0
    statistics_nfs_ops_raw_create_file_total_time: int = 0
    statistics_nfs_ops_raw_create_other_count: int = 0
    statistics_nfs_ops_raw_create_other_total_time: int = 0
    statistics_nfs_ops_raw_create_symlink_count: int = 0
    statistics_nfs_ops_raw_create_symlink_total_time: int = 0
    statistics_nfs_ops_raw_getattr_count: int = 0
    statistics_nfs_ops_raw_getattr_total_time: int = 0
    statistics_nfs_ops_raw_link_count: int = 0
    statistics_nfs_ops_raw_link_total_time: int = 0
    statistics_nfs_ops_raw_lock_count: int = 0
    statistics_nfs_ops_raw_lock_total_time: int = 0
    statistics_nfs_ops_raw_lookup_count: int = 0
    statistics_nfs_ops_raw_lookup_total_time: int = 0
    statistics_nfs_ops_raw_open_count: int = 0
    statistics_nfs_ops_raw_open_total_time: int = 0
    statistics_nfs_ops_raw_read_count: int = 0
    statistics_nfs_ops_raw_read_total_time: int = 0
    statistics_nfs_ops_raw_read_volume_protocol_latency_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_read_volume_protocol_latency_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_read_volume_protocol_size_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_read_volume_protocol_size_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_readdir_count: int = 0
    statistics_nfs_ops_raw_readdir_total_time: int = 0
    statistics_nfs_ops_raw_readlink_count: int = 0
    statistics_nfs_ops_raw_readlink_total_time: int = 0
    statistics_nfs_ops_raw_rename_count: int = 0
    statistics_nfs_ops_raw_rename_total_time: int = 0
    statistics_nfs_ops_raw_setattr_count: int = 0
    statistics_nfs_ops_raw_setattr_total_time: int = 0
    statistics_nfs_ops_raw_unlink_count: int = 0
    statistics_nfs_ops_raw_unlink_total_time: int = 0
    statistics_nfs_ops_raw_watch_count: int = 0
    statistics_nfs_ops_raw_watch_total_time: int = 0
    statistics_nfs_ops_raw_write_count: int = 0
    statistics_nfs_ops_raw_write_total_time: int = 0
    statistics_nfs_ops_raw_write_volume_protocol_latency_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_write_volume_protocol_latency_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_write_volume_protocol_size_histogram_counts: list[int] = Field(
        default_factory=list
    )
    statistics_nfs_ops_raw_write_volume_protocol_size_histogram_labels: list[str] = Field(
        default_factory=list
    )
    statistics_status: str = ""
    statistics_throughput_raw_other: int = 0
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    status: list[str] = Field(default_factory=list)
    style: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    tiering_min_cooling_days: int = 0
    tiering_object_tags: list[str] = Field(default_factory=list)
    tiering_policy: str = ""
    tiering_supported: bool = False
    type_: str = ""
    use_mirrored_aggregates: bool = False
    uuid: str = ""
    validate_only: bool = False
