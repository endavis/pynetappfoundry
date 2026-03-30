"""OntapAggregate information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAggregateSimulatedRaidGroup(OntapModel):
    """OntapAggregateSimulatedRaidGroup sub-model for simulated_raid_groups."""

    block_storage_hybrid_cache_simulated_raid_groups_added_data_disk_count: int = 0
    block_storage_hybrid_cache_simulated_raid_groups_added_parity_disk_count: int = 0
    block_storage_hybrid_cache_simulated_raid_groups_existing_data_disk_count: int = 0
    block_storage_hybrid_cache_simulated_raid_groups_existing_parity_disk_count: int = 0
    block_storage_hybrid_cache_simulated_raid_groups_is_partition: bool = False
    block_storage_hybrid_cache_simulated_raid_groups_name: str = ""
    block_storage_hybrid_cache_simulated_raid_groups_usable_size: int = 0


class OntapAggregateStoragePool(OntapModel):
    """OntapAggregateStoragePool sub-model for storage_pools."""

    block_storage_hybrid_cache_storage_pools_allocation_units_count: int = 0
    block_storage_hybrid_cache_storage_pools_storage_pool_name: str = ""
    block_storage_hybrid_cache_storage_pools_storage_pool_uuid: str = ""


class OntapAggregatePlex(OntapModel):
    """OntapAggregatePlex sub-model for plexes."""

    block_storage_plexes_name: str = ""


class OntapAggregateSimulatedRaidGroup2(OntapModel):
    """OntapAggregateSimulatedRaidGroup2 sub-model for simulated_raid_groups."""

    block_storage_primary_simulated_raid_groups_added_data_disk_count: int = 0
    block_storage_primary_simulated_raid_groups_added_parity_disk_count: int = 0
    block_storage_primary_simulated_raid_groups_data_disk_count: int = 0
    block_storage_primary_simulated_raid_groups_existing_data_disk_count: int = 0
    block_storage_primary_simulated_raid_groups_existing_parity_disk_count: int = 0
    block_storage_primary_simulated_raid_groups_is_partition: bool = False
    block_storage_primary_simulated_raid_groups_name: str = ""
    block_storage_primary_simulated_raid_groups_parity_disk_count: int = 0
    block_storage_primary_simulated_raid_groups_raid_type: str = ""
    block_storage_primary_simulated_raid_groups_usable_size: int = 0


class OntapAggregateStore(OntapModel):
    """OntapAggregateStore sub-model for stores."""

    cloud_storage_stores_cloud_store_name: str = ""
    cloud_storage_stores_cloud_store_uuid: str = ""
    cloud_storage_stores_used: int = 0


class OntapAggregate(OntapModel):
    """OntapAggregate information."""

    block_storage_hybrid_cache_disk_count: int = 0
    block_storage_hybrid_cache_disk_type: str = ""
    block_storage_hybrid_cache_enabled: bool = False
    block_storage_hybrid_cache_raid_size: int = 0
    block_storage_hybrid_cache_raid_type: str = ""
    block_storage_hybrid_cache_simulated_raid_groups: list[OntapAggregateSimulatedRaidGroup] = (
        Field(default_factory=list)
    )
    block_storage_hybrid_cache_size: int = 0
    block_storage_hybrid_cache_storage_pools: list[OntapAggregateStoragePool] = Field(
        default_factory=list
    )
    block_storage_hybrid_cache_used: int = 0
    block_storage_mirror_enabled: bool = False
    block_storage_mirror_state: str = ""
    block_storage_plexes: list[OntapAggregatePlex] = Field(default_factory=list)
    block_storage_primary_checksum_style: str = ""
    block_storage_primary_disk_class: str = ""
    block_storage_primary_disk_count: int = 0
    block_storage_primary_disk_type: str = ""
    block_storage_primary_raid_size: int = 0
    block_storage_primary_raid_type: str = ""
    block_storage_primary_simulated_raid_groups: list[OntapAggregateSimulatedRaidGroup2] = Field(
        default_factory=list
    )
    block_storage_storage_type: str = ""
    block_storage_uses_partitions: bool = False
    cloud_storage_attach_eligible: bool = False
    cloud_storage_migrate_threshold: int = 0
    cloud_storage_stores: list[OntapAggregateStore] = Field(default_factory=list)
    cloud_storage_tiering_fullness_threshold: int = 0
    create_time: str = ""
    data_encryption_drive_protection_enabled: bool = False
    data_encryption_software_encryption_enabled: bool = False
    dr_home_node_name: str = ""
    dr_home_node_uuid: str = ""
    home_node_name: str = ""
    home_node_uuid: str = ""
    inactive_data_reporting_enabled: bool = False
    inactive_data_reporting_start_time: str = ""
    inode_attributes_file_private_capacity: int = 0
    inode_attributes_file_public_capacity: int = 0
    inode_attributes_files_private_used: int = 0
    inode_attributes_files_total: int = 0
    inode_attributes_files_used: int = 0
    inode_attributes_max_files_available: int = 0
    inode_attributes_max_files_possible: int = 0
    inode_attributes_max_files_used: int = 0
    inode_attributes_used_percent: int = 0
    inode_attributes_version: int = 0
    is_spare_low: bool = False
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
    metric_throughput_other: int = 0
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    sidl_enabled: bool = False
    snaplock_type: str = ""
    snapshot_files_total: int = 0
    snapshot_files_used: int = 0
    snapshot_max_files_available: int = 0
    snapshot_max_files_used: int = 0
    space_block_storage_aggregate_metadata: int = 0
    space_block_storage_aggregate_metadata_percent: int = 0
    space_block_storage_available: int = 0
    space_block_storage_data_compacted_count: int = 0
    space_block_storage_data_compaction_space_saved: int = 0
    space_block_storage_data_compaction_space_saved_percent: int = 0
    space_block_storage_full_threshold_percent: int = 0
    space_block_storage_inactive_user_data: int = 0
    space_block_storage_inactive_user_data_percent: int = 0
    space_block_storage_physical_used: int = 0
    space_block_storage_physical_used_percent: int = 0
    space_block_storage_size: int = 0
    space_block_storage_used: int = 0
    space_block_storage_used_including_snapshot_reserve: int = 0
    space_block_storage_used_including_snapshot_reserve_percent: int = 0
    space_block_storage_used_percent: int = 0
    space_block_storage_volume_deduplication_shared_count: int = 0
    space_block_storage_volume_deduplication_space_saved: int = 0
    space_block_storage_volume_deduplication_space_saved_percent: int = 0
    space_block_storage_volume_footprints_percent: int = 0
    space_cloud_storage_used: int = 0
    space_efficiency_auto_adaptive_compression_savings: bool = False
    space_efficiency_cross_volume_background_dedupe: bool = False
    space_efficiency_cross_volume_dedupe_savings: bool = False
    space_efficiency_cross_volume_inline_dedupe: bool = False
    space_efficiency_enable_workload_informed_tsse: bool = False
    space_efficiency_logical_used: int = 0
    space_efficiency_ratio: float = 0.0
    space_efficiency_savings: int = 0
    space_efficiency_wise_tsse_min_used_capacity_pct: int = 0
    space_efficiency_without_snapshots_logical_used: int = 0
    space_efficiency_without_snapshots_ratio: float = 0.0
    space_efficiency_without_snapshots_savings: int = 0
    space_efficiency_without_snapshots_flexclones_logical_used: int = 0
    space_efficiency_without_snapshots_flexclones_ratio: float = 0.0
    space_efficiency_without_snapshots_flexclones_savings: int = 0
    space_footprint: int = 0
    space_snapshot_available: int = 0
    space_snapshot_reserve_percent: int = 0
    space_snapshot_total: int = 0
    space_snapshot_used: int = 0
    space_snapshot_used_percent: int = 0
    state: str = ""
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_other: int = 0
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    uuid: str = ""
    volume_count: int = 0
