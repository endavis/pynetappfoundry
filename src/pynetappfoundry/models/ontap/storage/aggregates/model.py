# ruff: noqa: E501
"""OntapAggregate information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAggregateBlockStorageHybridCacheSimulatedRaidGroup(OntapModel):
    """OntapAggregateBlockStorageHybridCacheSimulatedRaidGroup sub-model for simulated_raid_groups."""

    added_data_disk_count: int = 0
    added_parity_disk_count: int = 0
    existing_data_disk_count: int = 0
    existing_parity_disk_count: int = 0
    is_partition: bool = False
    name: str = ""
    usable_size: int = 0


class OntapAggregateBlockStorageHybridCacheStoragePoolStoragePool(OntapModel):
    """OntapAggregateBlockStorageHybridCacheStoragePoolStoragePool sub-model for storage_pool."""

    name: str = ""
    uuid: str = ""


class OntapAggregateBlockStorageHybridCacheStoragePool(OntapModel):
    """OntapAggregateBlockStorageHybridCacheStoragePool sub-model for storage_pools."""

    allocation_units_count: int = 0
    storage_pool: OntapAggregateBlockStorageHybridCacheStoragePoolStoragePool = Field(
        default_factory=OntapAggregateBlockStorageHybridCacheStoragePoolStoragePool
    )


class OntapAggregateBlockStorageHybridCache(OntapModel):
    """OntapAggregateBlockStorageHybridCache sub-model for hybrid_cache."""

    disk_count: int = 0
    disk_type: str = ""
    enabled: bool = False
    raid_size: int = 0
    raid_type: str = ""
    simulated_raid_groups: list[OntapAggregateBlockStorageHybridCacheSimulatedRaidGroup] = Field(
        default_factory=list
    )
    size: int = 0
    storage_pools: list[OntapAggregateBlockStorageHybridCacheStoragePool] = Field(
        default_factory=list
    )
    used: int = 0


class OntapAggregateBlockStorageMirror(OntapModel):
    """OntapAggregateBlockStorageMirror sub-model for mirror."""

    enabled: bool = False
    state: str = ""


class OntapAggregateBlockStoragePlex(OntapModel):
    """OntapAggregateBlockStoragePlex sub-model for plexes."""

    name: str = ""


class OntapAggregateBlockStoragePrimarySimulatedRaidGroup(OntapModel):
    """OntapAggregateBlockStoragePrimarySimulatedRaidGroup sub-model for simulated_raid_groups."""

    added_data_disk_count: int = 0
    added_parity_disk_count: int = 0
    data_disk_count: int = 0
    existing_data_disk_count: int = 0
    existing_parity_disk_count: int = 0
    is_partition: bool = False
    name: str = ""
    parity_disk_count: int = 0
    raid_type: str = ""
    usable_size: int = 0


class OntapAggregateBlockStoragePrimary(OntapModel):
    """OntapAggregateBlockStoragePrimary sub-model for primary."""

    checksum_style: str = ""
    disk_class: str = ""
    disk_count: int = 0
    disk_type: str = ""
    raid_size: int = 0
    raid_type: str = ""
    simulated_raid_groups: list[OntapAggregateBlockStoragePrimarySimulatedRaidGroup] = Field(
        default_factory=list
    )


class OntapAggregateBlockStorage(OntapModel):
    """OntapAggregateBlockStorage sub-model for block_storage."""

    hybrid_cache: OntapAggregateBlockStorageHybridCache = Field(
        default_factory=OntapAggregateBlockStorageHybridCache
    )
    mirror: OntapAggregateBlockStorageMirror = Field(
        default_factory=OntapAggregateBlockStorageMirror
    )
    plexes: list[OntapAggregateBlockStoragePlex] = Field(default_factory=list)
    primary: OntapAggregateBlockStoragePrimary = Field(
        default_factory=OntapAggregateBlockStoragePrimary
    )
    storage_type: str = ""
    uses_partitions: bool = False


class OntapAggregateCloudStorageStoreCloudStore(OntapModel):
    """OntapAggregateCloudStorageStoreCloudStore sub-model for cloud_store."""

    name: str = ""
    uuid: str = ""


class OntapAggregateCloudStorageStore(OntapModel):
    """OntapAggregateCloudStorageStore sub-model for stores."""

    cloud_store: OntapAggregateCloudStorageStoreCloudStore = Field(
        default_factory=OntapAggregateCloudStorageStoreCloudStore
    )
    used: int = 0


class OntapAggregateCloudStorage(OntapModel):
    """OntapAggregateCloudStorage sub-model for cloud_storage."""

    attach_eligible: bool = False
    migrate_threshold: int = 0
    stores: list[OntapAggregateCloudStorageStore] = Field(default_factory=list)
    tiering_fullness_threshold: int = 0


class OntapAggregateDataEncryption(OntapModel):
    """OntapAggregateDataEncryption sub-model for data_encryption."""

    drive_protection_enabled: bool = False
    software_encryption_enabled: bool = False


class OntapAggregateDrHomeNode(OntapModel):
    """OntapAggregateDrHomeNode sub-model for dr_home_node."""

    name: str = ""
    uuid: str = ""


class OntapAggregateHomeNode(OntapModel):
    """OntapAggregateHomeNode sub-model for home_node."""

    name: str = ""
    uuid: str = ""


class OntapAggregateInactiveDataReporting(OntapModel):
    """OntapAggregateInactiveDataReporting sub-model for inactive_data_reporting."""

    enabled: bool = False
    start_time: str = ""


class OntapAggregateInodeAttributes(OntapModel):
    """OntapAggregateInodeAttributes sub-model for inode_attributes."""

    file_private_capacity: int = 0
    file_public_capacity: int = 0
    files_private_used: int = 0
    files_total: int = 0
    files_used: int = 0
    max_files_available: int = 0
    max_files_possible: int = 0
    max_files_used: int = 0
    used_percent: int = 0
    version: int = 0


class OntapAggregateMetricIops(OntapModel):
    """OntapAggregateMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapAggregateMetricLatency(OntapModel):
    """OntapAggregateMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapAggregateMetricThroughput(OntapModel):
    """OntapAggregateMetricThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapAggregateMetric(OntapModel):
    """OntapAggregateMetric sub-model for metric."""

    duration: str = ""
    iops: OntapAggregateMetricIops = Field(default_factory=OntapAggregateMetricIops)
    latency: OntapAggregateMetricLatency = Field(default_factory=OntapAggregateMetricLatency)
    status: str = ""
    throughput: OntapAggregateMetricThroughput = Field(
        default_factory=OntapAggregateMetricThroughput
    )
    timestamp: str = ""


class OntapAggregateNode(OntapModel):
    """OntapAggregateNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapAggregateSnapshot(OntapModel):
    """OntapAggregateSnapshot sub-model for snapshot."""

    files_total: int = 0
    files_used: int = 0
    max_files_available: int = 0
    max_files_used: int = 0


class OntapAggregateSpaceBlockStorage(OntapModel):
    """OntapAggregateSpaceBlockStorage sub-model for block_storage."""

    aggregate_metadata: int = 0
    aggregate_metadata_percent: int = 0
    available: int = 0
    data_compacted_count: int = 0
    data_compaction_space_saved: int = 0
    data_compaction_space_saved_percent: int = 0
    full_threshold_percent: int = 0
    inactive_user_data: int = 0
    inactive_user_data_percent: int = 0
    physical_used: int = 0
    physical_used_percent: int = 0
    size: int = 0
    used: int = 0
    used_including_snapshot_reserve: int = 0
    used_including_snapshot_reserve_percent: int = 0
    used_percent: int = 0
    volume_deduplication_shared_count: int = 0
    volume_deduplication_space_saved: int = 0
    volume_deduplication_space_saved_percent: int = 0
    volume_footprints_percent: int = 0


class OntapAggregateSpaceCloudStorage(OntapModel):
    """OntapAggregateSpaceCloudStorage sub-model for cloud_storage."""

    used: int = 0


class OntapAggregateSpaceEfficiency(OntapModel):
    """OntapAggregateSpaceEfficiency sub-model for efficiency."""

    auto_adaptive_compression_savings: bool = False
    cross_volume_background_dedupe: bool = False
    cross_volume_dedupe_savings: bool = False
    cross_volume_inline_dedupe: bool = False
    enable_workload_informed_tsse: bool = False
    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0
    wise_tsse_min_used_capacity_pct: int = 0


class OntapAggregateSpaceEfficiencyWithoutSnapshots(OntapModel):
    """OntapAggregateSpaceEfficiencyWithoutSnapshots sub-model for efficiency_without_snapshots."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapAggregateSpaceEfficiencyWithoutSnapshotsFlexclones(OntapModel):
    """OntapAggregateSpaceEfficiencyWithoutSnapshotsFlexclones sub-model for efficiency_without_snapshots_flexclones."""

    logical_used: int = 0
    ratio: float = 0.0
    savings: int = 0


class OntapAggregateSpaceSnapshot(OntapModel):
    """OntapAggregateSpaceSnapshot sub-model for snapshot."""

    available: int = 0
    reserve_percent: int = 0
    total: int = 0
    used: int = 0
    used_percent: int = 0


class OntapAggregateSpace(OntapModel):
    """OntapAggregateSpace sub-model for space."""

    block_storage: OntapAggregateSpaceBlockStorage = Field(
        default_factory=OntapAggregateSpaceBlockStorage
    )
    cloud_storage: OntapAggregateSpaceCloudStorage = Field(
        default_factory=OntapAggregateSpaceCloudStorage
    )
    efficiency: OntapAggregateSpaceEfficiency = Field(default_factory=OntapAggregateSpaceEfficiency)
    efficiency_without_snapshots: OntapAggregateSpaceEfficiencyWithoutSnapshots = Field(
        default_factory=OntapAggregateSpaceEfficiencyWithoutSnapshots
    )
    efficiency_without_snapshots_flexclones: OntapAggregateSpaceEfficiencyWithoutSnapshotsFlexclones = Field(
        default_factory=OntapAggregateSpaceEfficiencyWithoutSnapshotsFlexclones
    )
    footprint: int = 0
    snapshot: OntapAggregateSpaceSnapshot = Field(default_factory=OntapAggregateSpaceSnapshot)


class OntapAggregateStatisticsIopsRaw(OntapModel):
    """OntapAggregateStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapAggregateStatisticsLatencyRaw(OntapModel):
    """OntapAggregateStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapAggregateStatisticsThroughputRaw(OntapModel):
    """OntapAggregateStatisticsThroughputRaw sub-model for throughput_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapAggregateStatistics(OntapModel):
    """OntapAggregateStatistics sub-model for statistics."""

    iops_raw: OntapAggregateStatisticsIopsRaw = Field(
        default_factory=OntapAggregateStatisticsIopsRaw
    )
    latency_raw: OntapAggregateStatisticsLatencyRaw = Field(
        default_factory=OntapAggregateStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapAggregateStatisticsThroughputRaw = Field(
        default_factory=OntapAggregateStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapAggregate(OntapModel):
    """OntapAggregate information."""

    block_storage: OntapAggregateBlockStorage = Field(default_factory=OntapAggregateBlockStorage)
    cloud_storage: OntapAggregateCloudStorage = Field(default_factory=OntapAggregateCloudStorage)
    create_time: str = ""
    data_encryption: OntapAggregateDataEncryption = Field(
        default_factory=OntapAggregateDataEncryption
    )
    dr_home_node: OntapAggregateDrHomeNode = Field(default_factory=OntapAggregateDrHomeNode)
    home_node: OntapAggregateHomeNode = Field(default_factory=OntapAggregateHomeNode)
    inactive_data_reporting: OntapAggregateInactiveDataReporting = Field(
        default_factory=OntapAggregateInactiveDataReporting
    )
    inode_attributes: OntapAggregateInodeAttributes = Field(
        default_factory=OntapAggregateInodeAttributes
    )
    is_spare_low: bool = False
    metric: OntapAggregateMetric = Field(default_factory=OntapAggregateMetric)
    name: str = ""
    node: OntapAggregateNode = Field(default_factory=OntapAggregateNode)
    sidl_enabled: bool = False
    snaplock_type: str = ""
    snapshot: OntapAggregateSnapshot = Field(default_factory=OntapAggregateSnapshot)
    space: OntapAggregateSpace = Field(default_factory=OntapAggregateSpace)
    state: str = ""
    statistics: OntapAggregateStatistics = Field(default_factory=OntapAggregateStatistics)
    uuid: str = ""
    volume_count: int = 0
