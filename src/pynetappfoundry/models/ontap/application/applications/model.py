# ruff: noqa: E501
"""OntapApplication information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationSvm(OntapModel):
    """OntapApplicationSvm sub-model for svm."""

    uuid: str = ""
    name: str = ""


class OntapApplicationRpoComponentRpoLocal(OntapModel):
    """OntapApplicationRpoComponentRpoLocal sub-model for local."""

    name: str = ""
    description: str = ""


class OntapApplicationRpoComponentRpoRemote(OntapModel):
    """OntapApplicationRpoComponentRpoRemote sub-model for remote."""

    name: str = ""
    description: str = ""


class OntapApplicationRpoComponentRpo(OntapModel):
    """OntapApplicationRpoComponentRpo sub-model for rpo."""

    local: OntapApplicationRpoComponentRpoLocal = Field(
        default_factory=OntapApplicationRpoComponentRpoLocal
    )
    remote: OntapApplicationRpoComponentRpoRemote = Field(
        default_factory=OntapApplicationRpoComponentRpoRemote
    )


class OntapApplicationRpoComponent(OntapModel):
    """OntapApplicationRpoComponent sub-model for components."""

    uuid: str = ""
    name: str = ""
    rpo: OntapApplicationRpoComponentRpo = Field(default_factory=OntapApplicationRpoComponentRpo)


class OntapApplicationRpoLocal(OntapModel):
    """OntapApplicationRpoLocal sub-model for local."""

    name: str = ""
    description: str = ""


class OntapApplicationRpoRemote(OntapModel):
    """OntapApplicationRpoRemote sub-model for remote."""

    name: str = ""
    description: str = ""


class OntapApplicationRpo(OntapModel):
    """OntapApplicationRpo sub-model for rpo."""

    components: list[OntapApplicationRpoComponent] = Field(default_factory=list)
    is_supported: bool = False
    local: OntapApplicationRpoLocal = Field(default_factory=OntapApplicationRpoLocal)
    remote: OntapApplicationRpoRemote = Field(default_factory=OntapApplicationRpoRemote)


class OntapApplicationStatisticsComponentIops(OntapModel):
    """OntapApplicationStatisticsComponentIops sub-model for iops."""

    per_tb: int = 0
    total: int = 0


class OntapApplicationStatisticsComponentLatency(OntapModel):
    """OntapApplicationStatisticsComponentLatency sub-model for latency."""

    average: int = 0
    raw: int = 0


class OntapApplicationStatisticsComponentSnapshot(OntapModel):
    """OntapApplicationStatisticsComponentSnapshot sub-model for snapshot."""

    reserve: int = 0
    used: int = 0


class OntapApplicationStatisticsComponentSpace(OntapModel):
    """OntapApplicationStatisticsComponentSpace sub-model for space."""

    available: int = 0
    logical_used: int = 0
    provisioned: int = 0
    reserved_unused: int = 0
    savings: int = 0
    used: int = 0
    used_excluding_reserves: int = 0
    used_percent: int = 0


class OntapApplicationStatisticsComponentStorageService(OntapModel):
    """OntapApplicationStatisticsComponentStorageService sub-model for storage_service."""

    uuid: str = ""
    name: str = ""


class OntapApplicationStatisticsComponent(OntapModel):
    """OntapApplicationStatisticsComponent sub-model for components."""

    uuid: str = ""
    name: str = ""
    iops: OntapApplicationStatisticsComponentIops = Field(
        default_factory=OntapApplicationStatisticsComponentIops
    )
    latency: OntapApplicationStatisticsComponentLatency = Field(
        default_factory=OntapApplicationStatisticsComponentLatency
    )
    shared_storage_pool: bool = False
    snapshot: OntapApplicationStatisticsComponentSnapshot = Field(
        default_factory=OntapApplicationStatisticsComponentSnapshot
    )
    space: OntapApplicationStatisticsComponentSpace = Field(
        default_factory=OntapApplicationStatisticsComponentSpace
    )
    statistics_incomplete: bool = False
    storage_service: OntapApplicationStatisticsComponentStorageService = Field(
        default_factory=OntapApplicationStatisticsComponentStorageService
    )


class OntapApplicationStatisticsIops(OntapModel):
    """OntapApplicationStatisticsIops sub-model for iops."""

    per_tb: int = 0
    total: int = 0


class OntapApplicationStatisticsLatency(OntapModel):
    """OntapApplicationStatisticsLatency sub-model for latency."""

    average: int = 0
    raw: int = 0


class OntapApplicationStatisticsSnapshot(OntapModel):
    """OntapApplicationStatisticsSnapshot sub-model for snapshot."""

    reserve: int = 0
    used: int = 0


class OntapApplicationStatisticsSpace(OntapModel):
    """OntapApplicationStatisticsSpace sub-model for space."""

    available: int = 0
    logical_used: int = 0
    provisioned: int = 0
    reserved_unused: int = 0
    savings: int = 0
    used: int = 0
    used_excluding_reserves: int = 0
    used_percent: int = 0


class OntapApplicationStatistics(OntapModel):
    """OntapApplicationStatistics sub-model for statistics."""

    components: list[OntapApplicationStatisticsComponent] = Field(default_factory=list)
    iops: OntapApplicationStatisticsIops = Field(default_factory=OntapApplicationStatisticsIops)
    latency: OntapApplicationStatisticsLatency = Field(
        default_factory=OntapApplicationStatisticsLatency
    )
    shared_storage_pool: bool = False
    snapshot: OntapApplicationStatisticsSnapshot = Field(
        default_factory=OntapApplicationStatisticsSnapshot
    )
    space: OntapApplicationStatisticsSpace = Field(default_factory=OntapApplicationStatisticsSpace)
    statistics_incomplete: bool = False


class OntapApplicationTemplate(OntapModel):
    """OntapApplicationTemplate sub-model for template."""

    name: str = ""
    protocol: str = ""
    version: int = 0


class OntapApplicationMongoDbOnSanDatasetStorageService(OntapModel):
    """OntapApplicationMongoDbOnSanDatasetStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationMongoDbOnSanDataset(OntapModel):
    """OntapApplicationMongoDbOnSanDataset sub-model for dataset."""

    element_count: int = 0
    replication_factor: int = 0
    size: int = 0
    storage_service: OntapApplicationMongoDbOnSanDatasetStorageService = Field(
        default_factory=OntapApplicationMongoDbOnSanDatasetStorageService
    )


class OntapApplicationMongoDbOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationMongoDbOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationMongoDbOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationMongoDbOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationMongoDbOnSanNewIgroup(OntapModel):
    """OntapApplicationMongoDbOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationMongoDbOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationMongoDbOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationMongoDbOnSanProtectionType(OntapModel):
    """OntapApplicationMongoDbOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationMongoDbOnSanSecondaryIgroup(OntapModel):
    """OntapApplicationMongoDbOnSanSecondaryIgroup sub-model for secondary_igroups."""

    name: str = ""


class OntapApplicationMongoDbOnSan(OntapModel):
    """OntapApplicationMongoDbOnSan sub-model for mongo_db_on_san."""

    dataset: OntapApplicationMongoDbOnSanDataset = Field(
        default_factory=OntapApplicationMongoDbOnSanDataset
    )
    new_igroups: list[OntapApplicationMongoDbOnSanNewIgroup] = Field(default_factory=list)
    os_type: str = ""
    primary_igroup_name: str = ""
    protection_type: OntapApplicationMongoDbOnSanProtectionType = Field(
        default_factory=OntapApplicationMongoDbOnSanProtectionType
    )
    secondary_igroups: list[OntapApplicationMongoDbOnSanSecondaryIgroup] = Field(
        default_factory=list
    )


class OntapApplicationNasApplicationComponentExportPolicy(OntapModel):
    """OntapApplicationNasApplicationComponentExportPolicy sub-model for export_policy."""

    name: str = ""
    id: int = 0


class OntapApplicationNasApplicationComponentFlexcacheOriginSvm(OntapModel):
    """OntapApplicationNasApplicationComponentFlexcacheOriginSvm sub-model for svm."""

    name: str = ""


class OntapApplicationNasApplicationComponentFlexcacheOriginComponent(OntapModel):
    """OntapApplicationNasApplicationComponentFlexcacheOriginComponent sub-model for component."""

    name: str = ""


class OntapApplicationNasApplicationComponentFlexcacheOrigin(OntapModel):
    """OntapApplicationNasApplicationComponentFlexcacheOrigin sub-model for origin."""

    svm: OntapApplicationNasApplicationComponentFlexcacheOriginSvm = Field(
        default_factory=OntapApplicationNasApplicationComponentFlexcacheOriginSvm
    )
    component: OntapApplicationNasApplicationComponentFlexcacheOriginComponent = Field(
        default_factory=OntapApplicationNasApplicationComponentFlexcacheOriginComponent
    )


class OntapApplicationNasApplicationComponentFlexcache(OntapModel):
    """OntapApplicationNasApplicationComponentFlexcache sub-model for flexcache."""

    dr_cache: bool = False
    origin: OntapApplicationNasApplicationComponentFlexcacheOrigin = Field(
        default_factory=OntapApplicationNasApplicationComponentFlexcacheOrigin
    )


class OntapApplicationNasApplicationComponentQosPolicy(OntapModel):
    """OntapApplicationNasApplicationComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationNasApplicationComponentQos(OntapModel):
    """OntapApplicationNasApplicationComponentQos sub-model for qos."""

    policy: OntapApplicationNasApplicationComponentQosPolicy = Field(
        default_factory=OntapApplicationNasApplicationComponentQosPolicy
    )


class OntapApplicationNasApplicationComponentSnaplockRetention(OntapModel):
    """OntapApplicationNasApplicationComponentSnaplockRetention sub-model for retention."""

    default: str = ""
    minimum: str = ""
    maximum: str = ""


class OntapApplicationNasApplicationComponentSnaplock(OntapModel):
    """OntapApplicationNasApplicationComponentSnaplock sub-model for snaplock."""

    append_mode_enabled: bool = False
    autocommit_period: str = ""
    retention: OntapApplicationNasApplicationComponentSnaplockRetention = Field(
        default_factory=OntapApplicationNasApplicationComponentSnaplockRetention
    )
    snaplock_type: str = ""


class OntapApplicationNasApplicationComponentStorageService(OntapModel):
    """OntapApplicationNasApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationNasApplicationComponentTieringObjectStore(OntapModel):
    """OntapApplicationNasApplicationComponentTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapApplicationNasApplicationComponentTiering(OntapModel):
    """OntapApplicationNasApplicationComponentTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapApplicationNasApplicationComponentTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapApplicationNasApplicationComponent(OntapModel):
    """OntapApplicationNasApplicationComponent sub-model for application_components."""

    name: str = ""
    export_policy: OntapApplicationNasApplicationComponentExportPolicy = Field(
        default_factory=OntapApplicationNasApplicationComponentExportPolicy
    )
    flexcache: OntapApplicationNasApplicationComponentFlexcache = Field(
        default_factory=OntapApplicationNasApplicationComponentFlexcache
    )
    qos: OntapApplicationNasApplicationComponentQos = Field(
        default_factory=OntapApplicationNasApplicationComponentQos
    )
    scale_out: bool = False
    share_count: int = 0
    snaplock: OntapApplicationNasApplicationComponentSnaplock = Field(
        default_factory=OntapApplicationNasApplicationComponentSnaplock
    )
    snapshot_locking_enabled: bool = False
    storage_service: OntapApplicationNasApplicationComponentStorageService = Field(
        default_factory=OntapApplicationNasApplicationComponentStorageService
    )
    tiering: OntapApplicationNasApplicationComponentTiering = Field(
        default_factory=OntapApplicationNasApplicationComponentTiering
    )
    total_size: int = 0


class OntapApplicationNasCifsAccess(OntapModel):
    """OntapApplicationNasCifsAccess sub-model for cifs_access."""

    access: str = ""
    user_or_group: str = ""


class OntapApplicationNasExcludeAggregate(OntapModel):
    """OntapApplicationNasExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationNasNfsAccess(OntapModel):
    """OntapApplicationNasNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationNasProtectionType(OntapModel):
    """OntapApplicationNasProtectionType sub-model for protection_type."""

    local_policy: str = ""
    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationNas(OntapModel):
    """OntapApplicationNas sub-model for nas."""

    application_components: list[OntapApplicationNasApplicationComponent] = Field(
        default_factory=list
    )
    cifs_access: list[OntapApplicationNasCifsAccess] = Field(default_factory=list)
    cifs_share_name: str = ""
    exclude_aggregates: list[OntapApplicationNasExcludeAggregate] = Field(default_factory=list)
    nfs_access: list[OntapApplicationNasNfsAccess] = Field(default_factory=list)
    protection_type: OntapApplicationNasProtectionType = Field(
        default_factory=OntapApplicationNasProtectionType
    )


class OntapApplicationNvmeComponentPerformanceStorageService(OntapModel):
    """OntapApplicationNvmeComponentPerformanceStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationNvmeComponentPerformance(OntapModel):
    """OntapApplicationNvmeComponentPerformance sub-model for performance."""

    storage_service: OntapApplicationNvmeComponentPerformanceStorageService = Field(
        default_factory=OntapApplicationNvmeComponentPerformanceStorageService
    )


class OntapApplicationNvmeComponentQosPolicy(OntapModel):
    """OntapApplicationNvmeComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationNvmeComponentQos(OntapModel):
    """OntapApplicationNvmeComponentQos sub-model for qos."""

    policy: OntapApplicationNvmeComponentQosPolicy = Field(
        default_factory=OntapApplicationNvmeComponentQosPolicy
    )


class OntapApplicationNvmeComponentSubsystemHostDhHmacChap(OntapModel):
    """OntapApplicationNvmeComponentSubsystemHostDhHmacChap sub-model for dh_hmac_chap."""

    controller_secret_key: str = ""
    group_size: str = ""
    hash_function: str = ""
    host_secret_key: str = ""


class OntapApplicationNvmeComponentSubsystemHost(OntapModel):
    """OntapApplicationNvmeComponentSubsystemHost sub-model for hosts."""

    dh_hmac_chap: OntapApplicationNvmeComponentSubsystemHostDhHmacChap = Field(
        default_factory=OntapApplicationNvmeComponentSubsystemHostDhHmacChap
    )
    nqn: str = ""
    priority: str = ""


class OntapApplicationNvmeComponentSubsystem(OntapModel):
    """OntapApplicationNvmeComponentSubsystem sub-model for subsystem."""

    uuid: str = ""
    name: str = ""
    hosts: list[OntapApplicationNvmeComponentSubsystemHost] = Field(default_factory=list)
    os_type: str = ""


class OntapApplicationNvmeComponentTieringObjectStore(OntapModel):
    """OntapApplicationNvmeComponentTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapApplicationNvmeComponentTiering(OntapModel):
    """OntapApplicationNvmeComponentTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapApplicationNvmeComponentTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapApplicationNvmeComponent(OntapModel):
    """OntapApplicationNvmeComponent sub-model for components."""

    name: str = ""
    namespace_count: int = 0
    os_type: str = ""
    performance: OntapApplicationNvmeComponentPerformance = Field(
        default_factory=OntapApplicationNvmeComponentPerformance
    )
    qos: OntapApplicationNvmeComponentQos = Field(default_factory=OntapApplicationNvmeComponentQos)
    subsystem: OntapApplicationNvmeComponentSubsystem = Field(
        default_factory=OntapApplicationNvmeComponentSubsystem
    )
    tiering: OntapApplicationNvmeComponentTiering = Field(
        default_factory=OntapApplicationNvmeComponentTiering
    )
    total_size: int = 0


class OntapApplicationNvmeRpoLocal(OntapModel):
    """OntapApplicationNvmeRpoLocal sub-model for local."""

    name: str = ""
    policy: str = ""


class OntapApplicationNvmeRpoRemote(OntapModel):
    """OntapApplicationNvmeRpoRemote sub-model for remote."""

    name: str = ""


class OntapApplicationNvmeRpo(OntapModel):
    """OntapApplicationNvmeRpo sub-model for rpo."""

    local: OntapApplicationNvmeRpoLocal = Field(default_factory=OntapApplicationNvmeRpoLocal)
    remote: OntapApplicationNvmeRpoRemote = Field(default_factory=OntapApplicationNvmeRpoRemote)


class OntapApplicationNvme(OntapModel):
    """OntapApplicationNvme sub-model for nvme."""

    components: list[OntapApplicationNvmeComponent] = Field(default_factory=list)
    os_type: str = ""
    rpo: OntapApplicationNvmeRpo = Field(default_factory=OntapApplicationNvmeRpo)


class OntapApplicationOracleOnNfsArchiveLogStorageService(OntapModel):
    """OntapApplicationOracleOnNfsArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnNfsArchiveLog(OntapModel):
    """OntapApplicationOracleOnNfsArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationOracleOnNfsArchiveLogStorageService = Field(
        default_factory=OntapApplicationOracleOnNfsArchiveLogStorageService
    )


class OntapApplicationOracleOnNfsDbStorageService(OntapModel):
    """OntapApplicationOracleOnNfsDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnNfsDb(OntapModel):
    """OntapApplicationOracleOnNfsDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationOracleOnNfsDbStorageService = Field(
        default_factory=OntapApplicationOracleOnNfsDbStorageService
    )


class OntapApplicationOracleOnNfsNfsAccess(OntapModel):
    """OntapApplicationOracleOnNfsNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationOracleOnNfsOraHomeStorageService(OntapModel):
    """OntapApplicationOracleOnNfsOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnNfsOraHome(OntapModel):
    """OntapApplicationOracleOnNfsOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationOracleOnNfsOraHomeStorageService = Field(
        default_factory=OntapApplicationOracleOnNfsOraHomeStorageService
    )


class OntapApplicationOracleOnNfsProtectionType(OntapModel):
    """OntapApplicationOracleOnNfsProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationOracleOnNfsRedoLogStorageService(OntapModel):
    """OntapApplicationOracleOnNfsRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnNfsRedoLog(OntapModel):
    """OntapApplicationOracleOnNfsRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationOracleOnNfsRedoLogStorageService = Field(
        default_factory=OntapApplicationOracleOnNfsRedoLogStorageService
    )


class OntapApplicationOracleOnNfs(OntapModel):
    """OntapApplicationOracleOnNfs sub-model for oracle_on_nfs."""

    archive_log: OntapApplicationOracleOnNfsArchiveLog = Field(
        default_factory=OntapApplicationOracleOnNfsArchiveLog
    )
    db: OntapApplicationOracleOnNfsDb = Field(default_factory=OntapApplicationOracleOnNfsDb)
    nfs_access: list[OntapApplicationOracleOnNfsNfsAccess] = Field(default_factory=list)
    ora_home: OntapApplicationOracleOnNfsOraHome = Field(
        default_factory=OntapApplicationOracleOnNfsOraHome
    )
    protection_type: OntapApplicationOracleOnNfsProtectionType = Field(
        default_factory=OntapApplicationOracleOnNfsProtectionType
    )
    redo_log: OntapApplicationOracleOnNfsRedoLog = Field(
        default_factory=OntapApplicationOracleOnNfsRedoLog
    )


class OntapApplicationOracleOnSanArchiveLogStorageService(OntapModel):
    """OntapApplicationOracleOnSanArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnSanArchiveLog(OntapModel):
    """OntapApplicationOracleOnSanArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationOracleOnSanArchiveLogStorageService = Field(
        default_factory=OntapApplicationOracleOnSanArchiveLogStorageService
    )


class OntapApplicationOracleOnSanDbStorageService(OntapModel):
    """OntapApplicationOracleOnSanDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnSanDb(OntapModel):
    """OntapApplicationOracleOnSanDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationOracleOnSanDbStorageService = Field(
        default_factory=OntapApplicationOracleOnSanDbStorageService
    )


class OntapApplicationOracleOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationOracleOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationOracleOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationOracleOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationOracleOnSanNewIgroup(OntapModel):
    """OntapApplicationOracleOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationOracleOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationOracleOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationOracleOnSanOraHomeStorageService(OntapModel):
    """OntapApplicationOracleOnSanOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnSanOraHome(OntapModel):
    """OntapApplicationOracleOnSanOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationOracleOnSanOraHomeStorageService = Field(
        default_factory=OntapApplicationOracleOnSanOraHomeStorageService
    )


class OntapApplicationOracleOnSanProtectionType(OntapModel):
    """OntapApplicationOracleOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationOracleOnSanRedoLogStorageService(OntapModel):
    """OntapApplicationOracleOnSanRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleOnSanRedoLog(OntapModel):
    """OntapApplicationOracleOnSanRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationOracleOnSanRedoLogStorageService = Field(
        default_factory=OntapApplicationOracleOnSanRedoLogStorageService
    )


class OntapApplicationOracleOnSan(OntapModel):
    """OntapApplicationOracleOnSan sub-model for oracle_on_san."""

    archive_log: OntapApplicationOracleOnSanArchiveLog = Field(
        default_factory=OntapApplicationOracleOnSanArchiveLog
    )
    db: OntapApplicationOracleOnSanDb = Field(default_factory=OntapApplicationOracleOnSanDb)
    igroup_name: str = ""
    new_igroups: list[OntapApplicationOracleOnSanNewIgroup] = Field(default_factory=list)
    ora_home: OntapApplicationOracleOnSanOraHome = Field(
        default_factory=OntapApplicationOracleOnSanOraHome
    )
    os_type: str = ""
    protection_type: OntapApplicationOracleOnSanProtectionType = Field(
        default_factory=OntapApplicationOracleOnSanProtectionType
    )
    redo_log: OntapApplicationOracleOnSanRedoLog = Field(
        default_factory=OntapApplicationOracleOnSanRedoLog
    )


class OntapApplicationOracleRacOnNfsArchiveLogStorageService(OntapModel):
    """OntapApplicationOracleRacOnNfsArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnNfsArchiveLog(OntapModel):
    """OntapApplicationOracleRacOnNfsArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnNfsArchiveLogStorageService = Field(
        default_factory=OntapApplicationOracleRacOnNfsArchiveLogStorageService
    )


class OntapApplicationOracleRacOnNfsDbStorageService(OntapModel):
    """OntapApplicationOracleRacOnNfsDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnNfsDb(OntapModel):
    """OntapApplicationOracleRacOnNfsDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnNfsDbStorageService = Field(
        default_factory=OntapApplicationOracleRacOnNfsDbStorageService
    )


class OntapApplicationOracleRacOnNfsGridBinaryStorageService(OntapModel):
    """OntapApplicationOracleRacOnNfsGridBinaryStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnNfsGridBinary(OntapModel):
    """OntapApplicationOracleRacOnNfsGridBinary sub-model for grid_binary."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnNfsGridBinaryStorageService = Field(
        default_factory=OntapApplicationOracleRacOnNfsGridBinaryStorageService
    )


class OntapApplicationOracleRacOnNfsNfsAccess(OntapModel):
    """OntapApplicationOracleRacOnNfsNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationOracleRacOnNfsOraHomeStorageService(OntapModel):
    """OntapApplicationOracleRacOnNfsOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnNfsOraHome(OntapModel):
    """OntapApplicationOracleRacOnNfsOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnNfsOraHomeStorageService = Field(
        default_factory=OntapApplicationOracleRacOnNfsOraHomeStorageService
    )


class OntapApplicationOracleRacOnNfsOracleCrsStorageService(OntapModel):
    """OntapApplicationOracleRacOnNfsOracleCrsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnNfsOracleCrs(OntapModel):
    """OntapApplicationOracleRacOnNfsOracleCrs sub-model for oracle_crs."""

    copies: int = 0
    size: int = 0
    storage_service: OntapApplicationOracleRacOnNfsOracleCrsStorageService = Field(
        default_factory=OntapApplicationOracleRacOnNfsOracleCrsStorageService
    )


class OntapApplicationOracleRacOnNfsProtectionType(OntapModel):
    """OntapApplicationOracleRacOnNfsProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationOracleRacOnNfsRedoLogStorageService(OntapModel):
    """OntapApplicationOracleRacOnNfsRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnNfsRedoLog(OntapModel):
    """OntapApplicationOracleRacOnNfsRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationOracleRacOnNfsRedoLogStorageService = Field(
        default_factory=OntapApplicationOracleRacOnNfsRedoLogStorageService
    )


class OntapApplicationOracleRacOnNfs(OntapModel):
    """OntapApplicationOracleRacOnNfs sub-model for oracle_rac_on_nfs."""

    archive_log: OntapApplicationOracleRacOnNfsArchiveLog = Field(
        default_factory=OntapApplicationOracleRacOnNfsArchiveLog
    )
    db: OntapApplicationOracleRacOnNfsDb = Field(default_factory=OntapApplicationOracleRacOnNfsDb)
    grid_binary: OntapApplicationOracleRacOnNfsGridBinary = Field(
        default_factory=OntapApplicationOracleRacOnNfsGridBinary
    )
    nfs_access: list[OntapApplicationOracleRacOnNfsNfsAccess] = Field(default_factory=list)
    ora_home: OntapApplicationOracleRacOnNfsOraHome = Field(
        default_factory=OntapApplicationOracleRacOnNfsOraHome
    )
    oracle_crs: OntapApplicationOracleRacOnNfsOracleCrs = Field(
        default_factory=OntapApplicationOracleRacOnNfsOracleCrs
    )
    protection_type: OntapApplicationOracleRacOnNfsProtectionType = Field(
        default_factory=OntapApplicationOracleRacOnNfsProtectionType
    )
    redo_log: OntapApplicationOracleRacOnNfsRedoLog = Field(
        default_factory=OntapApplicationOracleRacOnNfsRedoLog
    )


class OntapApplicationOracleRacOnSanArchiveLogStorageService(OntapModel):
    """OntapApplicationOracleRacOnSanArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnSanArchiveLog(OntapModel):
    """OntapApplicationOracleRacOnSanArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnSanArchiveLogStorageService = Field(
        default_factory=OntapApplicationOracleRacOnSanArchiveLogStorageService
    )


class OntapApplicationOracleRacOnSanDbStorageService(OntapModel):
    """OntapApplicationOracleRacOnSanDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnSanDb(OntapModel):
    """OntapApplicationOracleRacOnSanDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnSanDbStorageService = Field(
        default_factory=OntapApplicationOracleRacOnSanDbStorageService
    )


class OntapApplicationOracleRacOnSanDbSid(OntapModel):
    """OntapApplicationOracleRacOnSanDbSid sub-model for db_sids."""

    igroup_name: str = ""


class OntapApplicationOracleRacOnSanGridBinaryStorageService(OntapModel):
    """OntapApplicationOracleRacOnSanGridBinaryStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnSanGridBinary(OntapModel):
    """OntapApplicationOracleRacOnSanGridBinary sub-model for grid_binary."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnSanGridBinaryStorageService = Field(
        default_factory=OntapApplicationOracleRacOnSanGridBinaryStorageService
    )


class OntapApplicationOracleRacOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationOracleRacOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationOracleRacOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationOracleRacOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationOracleRacOnSanNewIgroup(OntapModel):
    """OntapApplicationOracleRacOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationOracleRacOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationOracleRacOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationOracleRacOnSanOraHomeStorageService(OntapModel):
    """OntapApplicationOracleRacOnSanOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnSanOraHome(OntapModel):
    """OntapApplicationOracleRacOnSanOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationOracleRacOnSanOraHomeStorageService = Field(
        default_factory=OntapApplicationOracleRacOnSanOraHomeStorageService
    )


class OntapApplicationOracleRacOnSanOracleCrsStorageService(OntapModel):
    """OntapApplicationOracleRacOnSanOracleCrsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnSanOracleCrs(OntapModel):
    """OntapApplicationOracleRacOnSanOracleCrs sub-model for oracle_crs."""

    copies: int = 0
    size: int = 0
    storage_service: OntapApplicationOracleRacOnSanOracleCrsStorageService = Field(
        default_factory=OntapApplicationOracleRacOnSanOracleCrsStorageService
    )


class OntapApplicationOracleRacOnSanProtectionType(OntapModel):
    """OntapApplicationOracleRacOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationOracleRacOnSanRedoLogStorageService(OntapModel):
    """OntapApplicationOracleRacOnSanRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationOracleRacOnSanRedoLog(OntapModel):
    """OntapApplicationOracleRacOnSanRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationOracleRacOnSanRedoLogStorageService = Field(
        default_factory=OntapApplicationOracleRacOnSanRedoLogStorageService
    )


class OntapApplicationOracleRacOnSan(OntapModel):
    """OntapApplicationOracleRacOnSan sub-model for oracle_rac_on_san."""

    archive_log: OntapApplicationOracleRacOnSanArchiveLog = Field(
        default_factory=OntapApplicationOracleRacOnSanArchiveLog
    )
    db: OntapApplicationOracleRacOnSanDb = Field(default_factory=OntapApplicationOracleRacOnSanDb)
    db_sids: list[OntapApplicationOracleRacOnSanDbSid] = Field(default_factory=list)
    grid_binary: OntapApplicationOracleRacOnSanGridBinary = Field(
        default_factory=OntapApplicationOracleRacOnSanGridBinary
    )
    new_igroups: list[OntapApplicationOracleRacOnSanNewIgroup] = Field(default_factory=list)
    ora_home: OntapApplicationOracleRacOnSanOraHome = Field(
        default_factory=OntapApplicationOracleRacOnSanOraHome
    )
    oracle_crs: OntapApplicationOracleRacOnSanOracleCrs = Field(
        default_factory=OntapApplicationOracleRacOnSanOracleCrs
    )
    os_type: str = ""
    protection_type: OntapApplicationOracleRacOnSanProtectionType = Field(
        default_factory=OntapApplicationOracleRacOnSanProtectionType
    )
    redo_log: OntapApplicationOracleRacOnSanRedoLog = Field(
        default_factory=OntapApplicationOracleRacOnSanRedoLog
    )


class OntapApplicationS3BucketApplicationComponentAccessPolicyCondition(OntapModel):
    """OntapApplicationS3BucketApplicationComponentAccessPolicyCondition sub-model for conditions."""

    delimiters: list[str] = Field(default_factory=list)
    max_keys: list[int] = Field(default_factory=list)
    operator: str = ""
    prefixes: list[str] = Field(default_factory=list)
    source_ips: list[str] = Field(default_factory=list)
    usernames: list[str] = Field(default_factory=list)


class OntapApplicationS3BucketApplicationComponentAccessPolicy(OntapModel):
    """OntapApplicationS3BucketApplicationComponentAccessPolicy sub-model for access_policies."""

    actions: list[str] = Field(default_factory=list)
    conditions: list[OntapApplicationS3BucketApplicationComponentAccessPolicyCondition] = Field(
        default_factory=list
    )
    effect: str = ""
    principals: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapApplicationS3BucketApplicationComponentExcludeAggregate(OntapModel):
    """OntapApplicationS3BucketApplicationComponentExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationS3BucketApplicationComponentQosPolicy(OntapModel):
    """OntapApplicationS3BucketApplicationComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationS3BucketApplicationComponentQos(OntapModel):
    """OntapApplicationS3BucketApplicationComponentQos sub-model for qos."""

    policy: OntapApplicationS3BucketApplicationComponentQosPolicy = Field(
        default_factory=OntapApplicationS3BucketApplicationComponentQosPolicy
    )


class OntapApplicationS3BucketApplicationComponentStorageService(OntapModel):
    """OntapApplicationS3BucketApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationS3BucketApplicationComponent(OntapModel):
    """OntapApplicationS3BucketApplicationComponent sub-model for application_components."""

    uuid: str = ""
    name: str = ""
    access_policies: list[OntapApplicationS3BucketApplicationComponentAccessPolicy] = Field(
        default_factory=list
    )
    bucket_endpoint_type: str = ""
    capacity_tier: bool = False
    comment: str = ""
    default_retention_period: str = ""
    exclude_aggregates: list[OntapApplicationS3BucketApplicationComponentExcludeAggregate] = Field(
        default_factory=list
    )
    nas_path: str = ""
    qos: OntapApplicationS3BucketApplicationComponentQos = Field(
        default_factory=OntapApplicationS3BucketApplicationComponentQos
    )
    retention_mode: str = ""
    size: int = 0
    storage_service: OntapApplicationS3BucketApplicationComponentStorageService = Field(
        default_factory=OntapApplicationS3BucketApplicationComponentStorageService
    )
    versioning_state: str = ""


class OntapApplicationS3BucketProtectionType(OntapModel):
    """OntapApplicationS3BucketProtectionType sub-model for protection_type."""

    remote_rpo: str = ""


class OntapApplicationS3Bucket(OntapModel):
    """OntapApplicationS3Bucket sub-model for s3_bucket."""

    application_components: list[OntapApplicationS3BucketApplicationComponent] = Field(
        default_factory=list
    )
    protection_type: OntapApplicationS3BucketProtectionType = Field(
        default_factory=OntapApplicationS3BucketProtectionType
    )


class OntapApplicationSanApplicationComponentQosPolicy(OntapModel):
    """OntapApplicationSanApplicationComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationSanApplicationComponentQos(OntapModel):
    """OntapApplicationSanApplicationComponentQos sub-model for qos."""

    policy: OntapApplicationSanApplicationComponentQosPolicy = Field(
        default_factory=OntapApplicationSanApplicationComponentQosPolicy
    )


class OntapApplicationSanApplicationComponentStorageService(OntapModel):
    """OntapApplicationSanApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSanApplicationComponentTieringObjectStore(OntapModel):
    """OntapApplicationSanApplicationComponentTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapApplicationSanApplicationComponentTiering(OntapModel):
    """OntapApplicationSanApplicationComponentTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapApplicationSanApplicationComponentTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapApplicationSanApplicationComponent(OntapModel):
    """OntapApplicationSanApplicationComponent sub-model for application_components."""

    name: str = ""
    igroup_name: str = ""
    lun_count: int = 0
    os_type: str = ""
    qos: OntapApplicationSanApplicationComponentQos = Field(
        default_factory=OntapApplicationSanApplicationComponentQos
    )
    storage_service: OntapApplicationSanApplicationComponentStorageService = Field(
        default_factory=OntapApplicationSanApplicationComponentStorageService
    )
    tiering: OntapApplicationSanApplicationComponentTiering = Field(
        default_factory=OntapApplicationSanApplicationComponentTiering
    )
    total_size: int = 0


class OntapApplicationSanExcludeAggregate(OntapModel):
    """OntapApplicationSanExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationSanNewIgroupIgroup(OntapModel):
    """OntapApplicationSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationSanNewIgroup(OntapModel):
    """OntapApplicationSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationSanProtectionType(OntapModel):
    """OntapApplicationSanProtectionType sub-model for protection_type."""

    local_policy: str = ""
    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationSan(OntapModel):
    """OntapApplicationSan sub-model for san."""

    application_components: list[OntapApplicationSanApplicationComponent] = Field(
        default_factory=list
    )
    exclude_aggregates: list[OntapApplicationSanExcludeAggregate] = Field(default_factory=list)
    new_igroups: list[OntapApplicationSanNewIgroup] = Field(default_factory=list)
    os_type: str = ""
    protection_type: OntapApplicationSanProtectionType = Field(
        default_factory=OntapApplicationSanProtectionType
    )


class OntapApplicationSqlOnSanDbStorageService(OntapModel):
    """OntapApplicationSqlOnSanDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSqlOnSanDb(OntapModel):
    """OntapApplicationSqlOnSanDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationSqlOnSanDbStorageService = Field(
        default_factory=OntapApplicationSqlOnSanDbStorageService
    )


class OntapApplicationSqlOnSanLogStorageService(OntapModel):
    """OntapApplicationSqlOnSanLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSqlOnSanLog(OntapModel):
    """OntapApplicationSqlOnSanLog sub-model for log."""

    size: int = 0
    storage_service: OntapApplicationSqlOnSanLogStorageService = Field(
        default_factory=OntapApplicationSqlOnSanLogStorageService
    )


class OntapApplicationSqlOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationSqlOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationSqlOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationSqlOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationSqlOnSanNewIgroup(OntapModel):
    """OntapApplicationSqlOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationSqlOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationSqlOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationSqlOnSanProtectionType(OntapModel):
    """OntapApplicationSqlOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationSqlOnSanTempDbStorageService(OntapModel):
    """OntapApplicationSqlOnSanTempDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSqlOnSanTempDb(OntapModel):
    """OntapApplicationSqlOnSanTempDb sub-model for temp_db."""

    size: int = 0
    storage_service: OntapApplicationSqlOnSanTempDbStorageService = Field(
        default_factory=OntapApplicationSqlOnSanTempDbStorageService
    )


class OntapApplicationSqlOnSan(OntapModel):
    """OntapApplicationSqlOnSan sub-model for sql_on_san."""

    db: OntapApplicationSqlOnSanDb = Field(default_factory=OntapApplicationSqlOnSanDb)
    igroup_name: str = ""
    log: OntapApplicationSqlOnSanLog = Field(default_factory=OntapApplicationSqlOnSanLog)
    new_igroups: list[OntapApplicationSqlOnSanNewIgroup] = Field(default_factory=list)
    os_type: str = ""
    protection_type: OntapApplicationSqlOnSanProtectionType = Field(
        default_factory=OntapApplicationSqlOnSanProtectionType
    )
    server_cores_count: int = 0
    temp_db: OntapApplicationSqlOnSanTempDb = Field(default_factory=OntapApplicationSqlOnSanTempDb)


class OntapApplicationSqlOnSmbAccess(OntapModel):
    """OntapApplicationSqlOnSmbAccess sub-model for access."""

    installer: str = ""
    service_account: str = ""


class OntapApplicationSqlOnSmbDbStorageService(OntapModel):
    """OntapApplicationSqlOnSmbDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSqlOnSmbDb(OntapModel):
    """OntapApplicationSqlOnSmbDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationSqlOnSmbDbStorageService = Field(
        default_factory=OntapApplicationSqlOnSmbDbStorageService
    )


class OntapApplicationSqlOnSmbLogStorageService(OntapModel):
    """OntapApplicationSqlOnSmbLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSqlOnSmbLog(OntapModel):
    """OntapApplicationSqlOnSmbLog sub-model for log."""

    size: int = 0
    storage_service: OntapApplicationSqlOnSmbLogStorageService = Field(
        default_factory=OntapApplicationSqlOnSmbLogStorageService
    )


class OntapApplicationSqlOnSmbProtectionType(OntapModel):
    """OntapApplicationSqlOnSmbProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationSqlOnSmbTempDbStorageService(OntapModel):
    """OntapApplicationSqlOnSmbTempDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationSqlOnSmbTempDb(OntapModel):
    """OntapApplicationSqlOnSmbTempDb sub-model for temp_db."""

    size: int = 0
    storage_service: OntapApplicationSqlOnSmbTempDbStorageService = Field(
        default_factory=OntapApplicationSqlOnSmbTempDbStorageService
    )


class OntapApplicationSqlOnSmb(OntapModel):
    """OntapApplicationSqlOnSmb sub-model for sql_on_smb."""

    access: OntapApplicationSqlOnSmbAccess = Field(default_factory=OntapApplicationSqlOnSmbAccess)
    db: OntapApplicationSqlOnSmbDb = Field(default_factory=OntapApplicationSqlOnSmbDb)
    log: OntapApplicationSqlOnSmbLog = Field(default_factory=OntapApplicationSqlOnSmbLog)
    protection_type: OntapApplicationSqlOnSmbProtectionType = Field(
        default_factory=OntapApplicationSqlOnSmbProtectionType
    )
    server_cores_count: int = 0
    temp_db: OntapApplicationSqlOnSmbTempDb = Field(default_factory=OntapApplicationSqlOnSmbTempDb)


class OntapApplicationVdiOnNasDesktopsStorageService(OntapModel):
    """OntapApplicationVdiOnNasDesktopsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationVdiOnNasDesktops(OntapModel):
    """OntapApplicationVdiOnNasDesktops sub-model for desktops."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationVdiOnNasDesktopsStorageService = Field(
        default_factory=OntapApplicationVdiOnNasDesktopsStorageService
    )


class OntapApplicationVdiOnNasHyperVAccess(OntapModel):
    """OntapApplicationVdiOnNasHyperVAccess sub-model for hyper_v_access."""

    service_account: str = ""


class OntapApplicationVdiOnNasNfsAccess(OntapModel):
    """OntapApplicationVdiOnNasNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationVdiOnNasProtectionType(OntapModel):
    """OntapApplicationVdiOnNasProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationVdiOnNas(OntapModel):
    """OntapApplicationVdiOnNas sub-model for vdi_on_nas."""

    desktops: OntapApplicationVdiOnNasDesktops = Field(
        default_factory=OntapApplicationVdiOnNasDesktops
    )
    hyper_v_access: OntapApplicationVdiOnNasHyperVAccess = Field(
        default_factory=OntapApplicationVdiOnNasHyperVAccess
    )
    nfs_access: list[OntapApplicationVdiOnNasNfsAccess] = Field(default_factory=list)
    protection_type: OntapApplicationVdiOnNasProtectionType = Field(
        default_factory=OntapApplicationVdiOnNasProtectionType
    )


class OntapApplicationVdiOnSanDesktopsStorageService(OntapModel):
    """OntapApplicationVdiOnSanDesktopsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationVdiOnSanDesktops(OntapModel):
    """OntapApplicationVdiOnSanDesktops sub-model for desktops."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationVdiOnSanDesktopsStorageService = Field(
        default_factory=OntapApplicationVdiOnSanDesktopsStorageService
    )


class OntapApplicationVdiOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationVdiOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationVdiOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationVdiOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationVdiOnSanNewIgroup(OntapModel):
    """OntapApplicationVdiOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationVdiOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationVdiOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    protocol: str = ""


class OntapApplicationVdiOnSanProtectionType(OntapModel):
    """OntapApplicationVdiOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationVdiOnSan(OntapModel):
    """OntapApplicationVdiOnSan sub-model for vdi_on_san."""

    desktops: OntapApplicationVdiOnSanDesktops = Field(
        default_factory=OntapApplicationVdiOnSanDesktops
    )
    hypervisor: str = ""
    igroup_name: str = ""
    new_igroups: list[OntapApplicationVdiOnSanNewIgroup] = Field(default_factory=list)
    protection_type: OntapApplicationVdiOnSanProtectionType = Field(
        default_factory=OntapApplicationVdiOnSanProtectionType
    )


class OntapApplicationVsiOnNasDatastoreStorageService(OntapModel):
    """OntapApplicationVsiOnNasDatastoreStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationVsiOnNasDatastore(OntapModel):
    """OntapApplicationVsiOnNasDatastore sub-model for datastore."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationVsiOnNasDatastoreStorageService = Field(
        default_factory=OntapApplicationVsiOnNasDatastoreStorageService
    )


class OntapApplicationVsiOnNasHyperVAccess(OntapModel):
    """OntapApplicationVsiOnNasHyperVAccess sub-model for hyper_v_access."""

    service_account: str = ""


class OntapApplicationVsiOnNasNfsAccess(OntapModel):
    """OntapApplicationVsiOnNasNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationVsiOnNasProtectionType(OntapModel):
    """OntapApplicationVsiOnNasProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationVsiOnNas(OntapModel):
    """OntapApplicationVsiOnNas sub-model for vsi_on_nas."""

    datastore: OntapApplicationVsiOnNasDatastore = Field(
        default_factory=OntapApplicationVsiOnNasDatastore
    )
    hyper_v_access: OntapApplicationVsiOnNasHyperVAccess = Field(
        default_factory=OntapApplicationVsiOnNasHyperVAccess
    )
    nfs_access: list[OntapApplicationVsiOnNasNfsAccess] = Field(default_factory=list)
    protection_type: OntapApplicationVsiOnNasProtectionType = Field(
        default_factory=OntapApplicationVsiOnNasProtectionType
    )


class OntapApplicationVsiOnSanDatastoreStorageService(OntapModel):
    """OntapApplicationVsiOnSanDatastoreStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationVsiOnSanDatastore(OntapModel):
    """OntapApplicationVsiOnSanDatastore sub-model for datastore."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationVsiOnSanDatastoreStorageService = Field(
        default_factory=OntapApplicationVsiOnSanDatastoreStorageService
    )


class OntapApplicationVsiOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationVsiOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationVsiOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationVsiOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationVsiOnSanNewIgroup(OntapModel):
    """OntapApplicationVsiOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationVsiOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationVsiOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    protocol: str = ""


class OntapApplicationVsiOnSanProtectionType(OntapModel):
    """OntapApplicationVsiOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationVsiOnSan(OntapModel):
    """OntapApplicationVsiOnSan sub-model for vsi_on_san."""

    datastore: OntapApplicationVsiOnSanDatastore = Field(
        default_factory=OntapApplicationVsiOnSanDatastore
    )
    hypervisor: str = ""
    igroup_name: str = ""
    new_igroups: list[OntapApplicationVsiOnSanNewIgroup] = Field(default_factory=list)
    protection_type: OntapApplicationVsiOnSanProtectionType = Field(
        default_factory=OntapApplicationVsiOnSanProtectionType
    )


class OntapApplication(OntapModel):
    """OntapApplication information."""

    svm: OntapApplicationSvm = Field(default_factory=OntapApplicationSvm)
    uuid: str = ""
    name: str = ""
    creation_timestamp: str = ""
    delete_data: bool = False
    generation: int = 0
    protection_granularity: str = ""
    rpo: OntapApplicationRpo = Field(default_factory=OntapApplicationRpo)
    smart_container: bool = False
    state: str = ""
    statistics: OntapApplicationStatistics = Field(default_factory=OntapApplicationStatistics)
    template: OntapApplicationTemplate = Field(default_factory=OntapApplicationTemplate)
    mongo_db_on_san: OntapApplicationMongoDbOnSan = Field(
        default_factory=OntapApplicationMongoDbOnSan
    )
    nas: OntapApplicationNas = Field(default_factory=OntapApplicationNas)
    nvme: OntapApplicationNvme = Field(default_factory=OntapApplicationNvme)
    oracle_on_nfs: OntapApplicationOracleOnNfs = Field(default_factory=OntapApplicationOracleOnNfs)
    oracle_on_san: OntapApplicationOracleOnSan = Field(default_factory=OntapApplicationOracleOnSan)
    oracle_rac_on_nfs: OntapApplicationOracleRacOnNfs = Field(
        default_factory=OntapApplicationOracleRacOnNfs
    )
    oracle_rac_on_san: OntapApplicationOracleRacOnSan = Field(
        default_factory=OntapApplicationOracleRacOnSan
    )
    s3_bucket: OntapApplicationS3Bucket = Field(default_factory=OntapApplicationS3Bucket)
    san: OntapApplicationSan = Field(default_factory=OntapApplicationSan)
    sql_on_san: OntapApplicationSqlOnSan = Field(default_factory=OntapApplicationSqlOnSan)
    sql_on_smb: OntapApplicationSqlOnSmb = Field(default_factory=OntapApplicationSqlOnSmb)
    vdi_on_nas: OntapApplicationVdiOnNas = Field(default_factory=OntapApplicationVdiOnNas)
    vdi_on_san: OntapApplicationVdiOnSan = Field(default_factory=OntapApplicationVdiOnSan)
    vsi_on_nas: OntapApplicationVsiOnNas = Field(default_factory=OntapApplicationVsiOnNas)
    vsi_on_san: OntapApplicationVsiOnSan = Field(default_factory=OntapApplicationVsiOnSan)
