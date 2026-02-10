"""Storage aggregate and volume models (/storage API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AggregateInfo(BaseModel):
    """Storage aggregate information."""

    model_config = ConfigDict(extra="allow")

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


class VolumeInfo(BaseModel):
    """Volume information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    state: str = ""  # online, offline, restricted
    type: str = ""  # rw, dp, ls
    style: str = ""  # flexvol, flexgroup
    size: int = 0  # bytes
    autosize_mode: str = ""  # off, grow, grow_shrink
    autosize_grow_threshold: int = 0  # percentage
    autosize_shrink_threshold: int = 0  # percentage
    autosize_maximum: int = 0  # bytes
    autosize_minimum: int = 0  # bytes
    files_maximum: int = 0
    tiering_policy: str = ""  # none, snapshot-only, auto, all
    tiering_minimum_cooling_days: int = 0
    aggregate: str = ""  # FlexVol aggregate name
    aggregates: list[str] = Field(default_factory=list)  # FlexGroup aggregates
    snapshot_policy: str = ""
    export_policy: str = ""
    junction_path: str = ""
    nas_security_style: str = ""  # unix, ntfs, mixed


class FlexCacheInfo(BaseModel):
    """FlexCache volume information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    path: str = ""
    size: int = 0  # bytes
    origins: list[str] = Field(default_factory=list)  # origin volume paths
    global_file_locking_enabled: bool = False
    dr_cache: bool = False


class SnapshotScheduleInfo(BaseModel):
    """Schedule entry within a snapshot policy."""

    model_config = ConfigDict(extra="allow")

    schedule: str = ""
    count: int = 0
    prefix: str = ""
    snapmirror_label: str = ""


class SnapshotPolicyInfo(BaseModel):
    """Snapshot policy information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    enabled: bool = True
    scope: str = ""  # cluster, svm
    schedules: list[SnapshotScheduleInfo] = Field(default_factory=list)


class QosPolicyInfo(BaseModel):
    """QoS policy information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    scope: str = ""  # cluster, svm
    policy_class: str = ""  # preset, user_defined, system_defined
    fixed_max_throughput_iops: int = 0
    fixed_max_throughput_mbps: int = 0
    adaptive_expected_iops: int = 0
    adaptive_peak_iops: int = 0
    adaptive_block_size: str = ""  # any, 4k, 8k, etc.
