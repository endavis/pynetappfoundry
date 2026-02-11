"""Aggregate information — /storage/aggregates."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class AggregateInfo(CacheModel):
    """Storage aggregate information."""

    uuid: str = ""
    name: str = ""
    node: str = ""
    state: str = ""
    type: str = ""  # hdd, ssd, hybrid
    total_size: int = 0  # bytes
    disk_count: int = 0
    disk_type: str = ""
    raid_type: str = ""
    # block_storage structural fields
    storage_type: str = ""  # hdd/hybrid/lun/ssd/vmdisk
    disk_class: str = ""  # capacity/performance/solid_state/virtual/archive/capacity_flash
    raid_size: int = 0  # max disks per RAID group
    checksum_style: str = ""  # block/advanced_zoned/mixed
    uses_partitions: bool = False  # root-data partitioning
    mirror_enabled: bool = False  # SyncMirror protection
    mirror_state: str = ""  # unmirrored/normal/degraded/resynchronizing/failed
    hybrid_cache_enabled: bool = False  # Flash Pool indicator
    # other structural fields
    snaplock_type: str = ""  # non_snaplock/compliance/enterprise
    home_node: str = ""  # home node (differs from node during takeover)
    dr_home_node: str = ""  # MetroCluster DR home node
    create_time: str = ""  # aggregate creation timestamp
    # config flags
    cloud_attach_eligible: bool = False  # FabricPool eligibility
    encryption_software: bool = False  # NAE enabled
    encryption_drive: bool = False  # SED enabled
    sidl_enabled: bool = False  # single-instance data logging
    inactive_data_reporting_enabled: bool = False  # inactive data reporting
    volume_count: int = 0  # number of volumes on the aggregate
    # expensive field (needs explicit API request)
    is_spare_low: bool = False  # disk pool health flag
