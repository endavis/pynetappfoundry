# ruff: noqa: E501
"""OntapApplicationTemplate information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationTemplateMongoDbOnSanDatasetStorageService(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanDatasetStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateMongoDbOnSanDataset(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanDataset sub-model for dataset."""

    element_count: int = 0
    replication_factor: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateMongoDbOnSanDatasetStorageService = Field(
        default_factory=OntapApplicationTemplateMongoDbOnSanDatasetStorageService
    )


class OntapApplicationTemplateMongoDbOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateMongoDbOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateMongoDbOnSanNewIgroup(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateMongoDbOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationTemplateMongoDbOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateMongoDbOnSanProtectionType(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateMongoDbOnSanSecondaryIgroup(OntapModel):
    """OntapApplicationTemplateMongoDbOnSanSecondaryIgroup sub-model for secondary_igroups."""

    name: str = ""


class OntapApplicationTemplateMongoDbOnSan(OntapModel):
    """OntapApplicationTemplateMongoDbOnSan sub-model for mongo_db_on_san."""

    dataset: OntapApplicationTemplateMongoDbOnSanDataset = Field(
        default_factory=OntapApplicationTemplateMongoDbOnSanDataset
    )
    new_igroups: list[OntapApplicationTemplateMongoDbOnSanNewIgroup] = Field(default_factory=list)
    os_type: str = ""
    primary_igroup_name: str = ""
    protection_type: OntapApplicationTemplateMongoDbOnSanProtectionType = Field(
        default_factory=OntapApplicationTemplateMongoDbOnSanProtectionType
    )
    secondary_igroups: list[OntapApplicationTemplateMongoDbOnSanSecondaryIgroup] = Field(
        default_factory=list
    )


class OntapApplicationTemplateNasApplicationComponentExportPolicy(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentExportPolicy sub-model for export_policy."""

    name: str = ""
    id: int = 0


class OntapApplicationTemplateNasApplicationComponentFlexcacheOriginSvm(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentFlexcacheOriginSvm sub-model for svm."""

    name: str = ""


class OntapApplicationTemplateNasApplicationComponentFlexcacheOriginComponent(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentFlexcacheOriginComponent sub-model for component."""

    name: str = ""


class OntapApplicationTemplateNasApplicationComponentFlexcacheOrigin(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentFlexcacheOrigin sub-model for origin."""

    svm: OntapApplicationTemplateNasApplicationComponentFlexcacheOriginSvm = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentFlexcacheOriginSvm
    )
    component: OntapApplicationTemplateNasApplicationComponentFlexcacheOriginComponent = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentFlexcacheOriginComponent
    )


class OntapApplicationTemplateNasApplicationComponentFlexcache(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentFlexcache sub-model for flexcache."""

    dr_cache: bool = False
    origin: OntapApplicationTemplateNasApplicationComponentFlexcacheOrigin = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentFlexcacheOrigin
    )


class OntapApplicationTemplateNasApplicationComponentQosPolicy(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateNasApplicationComponentQos(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentQos sub-model for qos."""

    policy: OntapApplicationTemplateNasApplicationComponentQosPolicy = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentQosPolicy
    )


class OntapApplicationTemplateNasApplicationComponentSnaplockRetention(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentSnaplockRetention sub-model for retention."""

    default: str = ""
    minimum: str = ""
    maximum: str = ""


class OntapApplicationTemplateNasApplicationComponentSnaplock(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentSnaplock sub-model for snaplock."""

    append_mode_enabled: bool = False
    autocommit_period: str = ""
    retention: OntapApplicationTemplateNasApplicationComponentSnaplockRetention = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentSnaplockRetention
    )
    snaplock_type: str = ""


class OntapApplicationTemplateNasApplicationComponentStorageService(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateNasApplicationComponentTieringObjectStore(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapApplicationTemplateNasApplicationComponentTiering(OntapModel):
    """OntapApplicationTemplateNasApplicationComponentTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapApplicationTemplateNasApplicationComponentTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapApplicationTemplateNasApplicationComponent(OntapModel):
    """OntapApplicationTemplateNasApplicationComponent sub-model for application_components."""

    name: str = ""
    export_policy: OntapApplicationTemplateNasApplicationComponentExportPolicy = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentExportPolicy
    )
    flexcache: OntapApplicationTemplateNasApplicationComponentFlexcache = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentFlexcache
    )
    qos: OntapApplicationTemplateNasApplicationComponentQos = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentQos
    )
    scale_out: bool = False
    share_count: int = 0
    snaplock: OntapApplicationTemplateNasApplicationComponentSnaplock = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentSnaplock
    )
    snapshot_locking_enabled: bool = False
    storage_service: OntapApplicationTemplateNasApplicationComponentStorageService = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentStorageService
    )
    tiering: OntapApplicationTemplateNasApplicationComponentTiering = Field(
        default_factory=OntapApplicationTemplateNasApplicationComponentTiering
    )
    total_size: int = 0


class OntapApplicationTemplateNasCifsAccess(OntapModel):
    """OntapApplicationTemplateNasCifsAccess sub-model for cifs_access."""

    access: str = ""
    user_or_group: str = ""


class OntapApplicationTemplateNasExcludeAggregate(OntapModel):
    """OntapApplicationTemplateNasExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateNasNfsAccess(OntapModel):
    """OntapApplicationTemplateNasNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateNasProtectionType(OntapModel):
    """OntapApplicationTemplateNasProtectionType sub-model for protection_type."""

    local_policy: str = ""
    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateNas(OntapModel):
    """OntapApplicationTemplateNas sub-model for nas."""

    application_components: list[OntapApplicationTemplateNasApplicationComponent] = Field(
        default_factory=list
    )
    cifs_access: list[OntapApplicationTemplateNasCifsAccess] = Field(default_factory=list)
    cifs_share_name: str = ""
    exclude_aggregates: list[OntapApplicationTemplateNasExcludeAggregate] = Field(
        default_factory=list
    )
    nfs_access: list[OntapApplicationTemplateNasNfsAccess] = Field(default_factory=list)
    protection_type: OntapApplicationTemplateNasProtectionType = Field(
        default_factory=OntapApplicationTemplateNasProtectionType
    )


class OntapApplicationTemplateNvmeComponentPerformanceStorageService(OntapModel):
    """OntapApplicationTemplateNvmeComponentPerformanceStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateNvmeComponentPerformance(OntapModel):
    """OntapApplicationTemplateNvmeComponentPerformance sub-model for performance."""

    storage_service: OntapApplicationTemplateNvmeComponentPerformanceStorageService = Field(
        default_factory=OntapApplicationTemplateNvmeComponentPerformanceStorageService
    )


class OntapApplicationTemplateNvmeComponentQosPolicy(OntapModel):
    """OntapApplicationTemplateNvmeComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateNvmeComponentQos(OntapModel):
    """OntapApplicationTemplateNvmeComponentQos sub-model for qos."""

    policy: OntapApplicationTemplateNvmeComponentQosPolicy = Field(
        default_factory=OntapApplicationTemplateNvmeComponentQosPolicy
    )


class OntapApplicationTemplateNvmeComponentSubsystemHostDhHmacChap(OntapModel):
    """OntapApplicationTemplateNvmeComponentSubsystemHostDhHmacChap sub-model for dh_hmac_chap."""

    controller_secret_key: str = ""
    group_size: str = ""
    hash_function: str = ""
    host_secret_key: str = ""


class OntapApplicationTemplateNvmeComponentSubsystemHost(OntapModel):
    """OntapApplicationTemplateNvmeComponentSubsystemHost sub-model for hosts."""

    dh_hmac_chap: OntapApplicationTemplateNvmeComponentSubsystemHostDhHmacChap = Field(
        default_factory=OntapApplicationTemplateNvmeComponentSubsystemHostDhHmacChap
    )
    nqn: str = ""
    priority: str = ""


class OntapApplicationTemplateNvmeComponentSubsystem(OntapModel):
    """OntapApplicationTemplateNvmeComponentSubsystem sub-model for subsystem."""

    uuid: str = ""
    name: str = ""
    hosts: list[OntapApplicationTemplateNvmeComponentSubsystemHost] = Field(default_factory=list)
    os_type: str = ""


class OntapApplicationTemplateNvmeComponentTieringObjectStore(OntapModel):
    """OntapApplicationTemplateNvmeComponentTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapApplicationTemplateNvmeComponentTiering(OntapModel):
    """OntapApplicationTemplateNvmeComponentTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapApplicationTemplateNvmeComponentTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapApplicationTemplateNvmeComponent(OntapModel):
    """OntapApplicationTemplateNvmeComponent sub-model for components."""

    name: str = ""
    namespace_count: int = 0
    os_type: str = ""
    performance: OntapApplicationTemplateNvmeComponentPerformance = Field(
        default_factory=OntapApplicationTemplateNvmeComponentPerformance
    )
    qos: OntapApplicationTemplateNvmeComponentQos = Field(
        default_factory=OntapApplicationTemplateNvmeComponentQos
    )
    subsystem: OntapApplicationTemplateNvmeComponentSubsystem = Field(
        default_factory=OntapApplicationTemplateNvmeComponentSubsystem
    )
    tiering: OntapApplicationTemplateNvmeComponentTiering = Field(
        default_factory=OntapApplicationTemplateNvmeComponentTiering
    )
    total_size: int = 0


class OntapApplicationTemplateNvmeRpoLocal(OntapModel):
    """OntapApplicationTemplateNvmeRpoLocal sub-model for local."""

    name: str = ""
    policy: str = ""


class OntapApplicationTemplateNvmeRpoRemote(OntapModel):
    """OntapApplicationTemplateNvmeRpoRemote sub-model for remote."""

    name: str = ""


class OntapApplicationTemplateNvmeRpo(OntapModel):
    """OntapApplicationTemplateNvmeRpo sub-model for rpo."""

    local: OntapApplicationTemplateNvmeRpoLocal = Field(
        default_factory=OntapApplicationTemplateNvmeRpoLocal
    )
    remote: OntapApplicationTemplateNvmeRpoRemote = Field(
        default_factory=OntapApplicationTemplateNvmeRpoRemote
    )


class OntapApplicationTemplateNvme(OntapModel):
    """OntapApplicationTemplateNvme sub-model for nvme."""

    components: list[OntapApplicationTemplateNvmeComponent] = Field(default_factory=list)
    os_type: str = ""
    rpo: OntapApplicationTemplateNvmeRpo = Field(default_factory=OntapApplicationTemplateNvmeRpo)


class OntapApplicationTemplateOracleOnNfsArchiveLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnNfsArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnNfsArchiveLog(OntapModel):
    """OntapApplicationTemplateOracleOnNfsArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnNfsArchiveLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsArchiveLogStorageService
    )


class OntapApplicationTemplateOracleOnNfsDbStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnNfsDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnNfsDb(OntapModel):
    """OntapApplicationTemplateOracleOnNfsDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnNfsDbStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsDbStorageService
    )


class OntapApplicationTemplateOracleOnNfsNfsAccess(OntapModel):
    """OntapApplicationTemplateOracleOnNfsNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateOracleOnNfsOraHomeStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnNfsOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnNfsOraHome(OntapModel):
    """OntapApplicationTemplateOracleOnNfsOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnNfsOraHomeStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsOraHomeStorageService
    )


class OntapApplicationTemplateOracleOnNfsProtectionType(OntapModel):
    """OntapApplicationTemplateOracleOnNfsProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateOracleOnNfsRedoLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnNfsRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnNfsRedoLog(OntapModel):
    """OntapApplicationTemplateOracleOnNfsRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnNfsRedoLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsRedoLogStorageService
    )


class OntapApplicationTemplateOracleOnNfs(OntapModel):
    """OntapApplicationTemplateOracleOnNfs sub-model for oracle_on_nfs."""

    archive_log: OntapApplicationTemplateOracleOnNfsArchiveLog = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsArchiveLog
    )
    db: OntapApplicationTemplateOracleOnNfsDb = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsDb
    )
    nfs_access: list[OntapApplicationTemplateOracleOnNfsNfsAccess] = Field(default_factory=list)
    ora_home: OntapApplicationTemplateOracleOnNfsOraHome = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsOraHome
    )
    protection_type: OntapApplicationTemplateOracleOnNfsProtectionType = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsProtectionType
    )
    redo_log: OntapApplicationTemplateOracleOnNfsRedoLog = Field(
        default_factory=OntapApplicationTemplateOracleOnNfsRedoLog
    )


class OntapApplicationTemplateOracleOnSanArchiveLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnSanArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnSanArchiveLog(OntapModel):
    """OntapApplicationTemplateOracleOnSanArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnSanArchiveLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnSanArchiveLogStorageService
    )


class OntapApplicationTemplateOracleOnSanDbStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnSanDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnSanDb(OntapModel):
    """OntapApplicationTemplateOracleOnSanDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnSanDbStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnSanDbStorageService
    )


class OntapApplicationTemplateOracleOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateOracleOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateOracleOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateOracleOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateOracleOnSanNewIgroup(OntapModel):
    """OntapApplicationTemplateOracleOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateOracleOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationTemplateOracleOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateOracleOnSanOraHomeStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnSanOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnSanOraHome(OntapModel):
    """OntapApplicationTemplateOracleOnSanOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnSanOraHomeStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnSanOraHomeStorageService
    )


class OntapApplicationTemplateOracleOnSanProtectionType(OntapModel):
    """OntapApplicationTemplateOracleOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateOracleOnSanRedoLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleOnSanRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleOnSanRedoLog(OntapModel):
    """OntapApplicationTemplateOracleOnSanRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationTemplateOracleOnSanRedoLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleOnSanRedoLogStorageService
    )


class OntapApplicationTemplateOracleOnSan(OntapModel):
    """OntapApplicationTemplateOracleOnSan sub-model for oracle_on_san."""

    archive_log: OntapApplicationTemplateOracleOnSanArchiveLog = Field(
        default_factory=OntapApplicationTemplateOracleOnSanArchiveLog
    )
    db: OntapApplicationTemplateOracleOnSanDb = Field(
        default_factory=OntapApplicationTemplateOracleOnSanDb
    )
    igroup_name: str = ""
    new_igroups: list[OntapApplicationTemplateOracleOnSanNewIgroup] = Field(default_factory=list)
    ora_home: OntapApplicationTemplateOracleOnSanOraHome = Field(
        default_factory=OntapApplicationTemplateOracleOnSanOraHome
    )
    os_type: str = ""
    protection_type: OntapApplicationTemplateOracleOnSanProtectionType = Field(
        default_factory=OntapApplicationTemplateOracleOnSanProtectionType
    )
    redo_log: OntapApplicationTemplateOracleOnSanRedoLog = Field(
        default_factory=OntapApplicationTemplateOracleOnSanRedoLog
    )


class OntapApplicationTemplateOracleRacOnNfsArchiveLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnNfsArchiveLog(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnNfsArchiveLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsArchiveLogStorageService
    )


class OntapApplicationTemplateOracleRacOnNfsDbStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnNfsDb(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnNfsDbStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsDbStorageService
    )


class OntapApplicationTemplateOracleRacOnNfsGridBinaryStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsGridBinaryStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnNfsGridBinary(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsGridBinary sub-model for grid_binary."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnNfsGridBinaryStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsGridBinaryStorageService
    )


class OntapApplicationTemplateOracleRacOnNfsNfsAccess(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateOracleRacOnNfsOraHomeStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnNfsOraHome(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnNfsOraHomeStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsOraHomeStorageService
    )


class OntapApplicationTemplateOracleRacOnNfsOracleCrsStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsOracleCrsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnNfsOracleCrs(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsOracleCrs sub-model for oracle_crs."""

    copies: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnNfsOracleCrsStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsOracleCrsStorageService
    )


class OntapApplicationTemplateOracleRacOnNfsProtectionType(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateOracleRacOnNfsRedoLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnNfsRedoLog(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfsRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnNfsRedoLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsRedoLogStorageService
    )


class OntapApplicationTemplateOracleRacOnNfs(OntapModel):
    """OntapApplicationTemplateOracleRacOnNfs sub-model for oracle_rac_on_nfs."""

    archive_log: OntapApplicationTemplateOracleRacOnNfsArchiveLog = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsArchiveLog
    )
    db: OntapApplicationTemplateOracleRacOnNfsDb = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsDb
    )
    grid_binary: OntapApplicationTemplateOracleRacOnNfsGridBinary = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsGridBinary
    )
    nfs_access: list[OntapApplicationTemplateOracleRacOnNfsNfsAccess] = Field(default_factory=list)
    ora_home: OntapApplicationTemplateOracleRacOnNfsOraHome = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsOraHome
    )
    oracle_crs: OntapApplicationTemplateOracleRacOnNfsOracleCrs = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsOracleCrs
    )
    protection_type: OntapApplicationTemplateOracleRacOnNfsProtectionType = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsProtectionType
    )
    redo_log: OntapApplicationTemplateOracleRacOnNfsRedoLog = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfsRedoLog
    )


class OntapApplicationTemplateOracleRacOnSanArchiveLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanArchiveLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnSanArchiveLog(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanArchiveLog sub-model for archive_log."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnSanArchiveLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanArchiveLogStorageService
    )


class OntapApplicationTemplateOracleRacOnSanDbStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnSanDb(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnSanDbStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanDbStorageService
    )


class OntapApplicationTemplateOracleRacOnSanDbSid(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanDbSid sub-model for db_sids."""

    igroup_name: str = ""


class OntapApplicationTemplateOracleRacOnSanGridBinaryStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanGridBinaryStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnSanGridBinary(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanGridBinary sub-model for grid_binary."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnSanGridBinaryStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanGridBinaryStorageService
    )


class OntapApplicationTemplateOracleRacOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateOracleRacOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateOracleRacOnSanNewIgroup(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateOracleRacOnSanNewIgroupIgroup] = Field(
        default_factory=list
    )
    initiator_objects: list[OntapApplicationTemplateOracleRacOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateOracleRacOnSanOraHomeStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanOraHomeStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnSanOraHome(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanOraHome sub-model for ora_home."""

    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnSanOraHomeStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanOraHomeStorageService
    )


class OntapApplicationTemplateOracleRacOnSanOracleCrsStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanOracleCrsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnSanOracleCrs(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanOracleCrs sub-model for oracle_crs."""

    copies: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnSanOracleCrsStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanOracleCrsStorageService
    )


class OntapApplicationTemplateOracleRacOnSanProtectionType(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateOracleRacOnSanRedoLogStorageService(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanRedoLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateOracleRacOnSanRedoLog(OntapModel):
    """OntapApplicationTemplateOracleRacOnSanRedoLog sub-model for redo_log."""

    mirrored: bool = False
    size: int = 0
    storage_service: OntapApplicationTemplateOracleRacOnSanRedoLogStorageService = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanRedoLogStorageService
    )


class OntapApplicationTemplateOracleRacOnSan(OntapModel):
    """OntapApplicationTemplateOracleRacOnSan sub-model for oracle_rac_on_san."""

    archive_log: OntapApplicationTemplateOracleRacOnSanArchiveLog = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanArchiveLog
    )
    db: OntapApplicationTemplateOracleRacOnSanDb = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanDb
    )
    db_sids: list[OntapApplicationTemplateOracleRacOnSanDbSid] = Field(default_factory=list)
    grid_binary: OntapApplicationTemplateOracleRacOnSanGridBinary = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanGridBinary
    )
    new_igroups: list[OntapApplicationTemplateOracleRacOnSanNewIgroup] = Field(default_factory=list)
    ora_home: OntapApplicationTemplateOracleRacOnSanOraHome = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanOraHome
    )
    oracle_crs: OntapApplicationTemplateOracleRacOnSanOracleCrs = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanOracleCrs
    )
    os_type: str = ""
    protection_type: OntapApplicationTemplateOracleRacOnSanProtectionType = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanProtectionType
    )
    redo_log: OntapApplicationTemplateOracleRacOnSanRedoLog = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSanRedoLog
    )


class OntapApplicationTemplateS3BucketApplicationComponentAccessPolicyCondition(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponentAccessPolicyCondition sub-model for conditions."""

    delimiters: list[str] = Field(default_factory=list)
    max_keys: list[int] = Field(default_factory=list)
    operator: str = ""
    prefixes: list[str] = Field(default_factory=list)
    source_ips: list[str] = Field(default_factory=list)
    usernames: list[str] = Field(default_factory=list)


class OntapApplicationTemplateS3BucketApplicationComponentAccessPolicy(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponentAccessPolicy sub-model for access_policies."""

    actions: list[str] = Field(default_factory=list)
    conditions: list[OntapApplicationTemplateS3BucketApplicationComponentAccessPolicyCondition] = (
        Field(default_factory=list)
    )
    effect: str = ""
    principals: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapApplicationTemplateS3BucketApplicationComponentExcludeAggregate(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponentExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateS3BucketApplicationComponentQosPolicy(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateS3BucketApplicationComponentQos(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponentQos sub-model for qos."""

    policy: OntapApplicationTemplateS3BucketApplicationComponentQosPolicy = Field(
        default_factory=OntapApplicationTemplateS3BucketApplicationComponentQosPolicy
    )


class OntapApplicationTemplateS3BucketApplicationComponentStorageService(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateS3BucketApplicationComponent(OntapModel):
    """OntapApplicationTemplateS3BucketApplicationComponent sub-model for application_components."""

    uuid: str = ""
    name: str = ""
    access_policies: list[OntapApplicationTemplateS3BucketApplicationComponentAccessPolicy] = Field(
        default_factory=list
    )
    bucket_endpoint_type: str = ""
    capacity_tier: bool = False
    comment: str = ""
    default_retention_period: str = ""
    exclude_aggregates: list[
        OntapApplicationTemplateS3BucketApplicationComponentExcludeAggregate
    ] = Field(default_factory=list)
    nas_path: str = ""
    qos: OntapApplicationTemplateS3BucketApplicationComponentQos = Field(
        default_factory=OntapApplicationTemplateS3BucketApplicationComponentQos
    )
    retention_mode: str = ""
    size: int = 0
    storage_service: OntapApplicationTemplateS3BucketApplicationComponentStorageService = Field(
        default_factory=OntapApplicationTemplateS3BucketApplicationComponentStorageService
    )
    versioning_state: str = ""


class OntapApplicationTemplateS3BucketProtectionType(OntapModel):
    """OntapApplicationTemplateS3BucketProtectionType sub-model for protection_type."""

    remote_rpo: str = ""


class OntapApplicationTemplateS3Bucket(OntapModel):
    """OntapApplicationTemplateS3Bucket sub-model for s3_bucket."""

    application_components: list[OntapApplicationTemplateS3BucketApplicationComponent] = Field(
        default_factory=list
    )
    protection_type: OntapApplicationTemplateS3BucketProtectionType = Field(
        default_factory=OntapApplicationTemplateS3BucketProtectionType
    )


class OntapApplicationTemplateSanApplicationComponentQosPolicy(OntapModel):
    """OntapApplicationTemplateSanApplicationComponentQosPolicy sub-model for policy."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateSanApplicationComponentQos(OntapModel):
    """OntapApplicationTemplateSanApplicationComponentQos sub-model for qos."""

    policy: OntapApplicationTemplateSanApplicationComponentQosPolicy = Field(
        default_factory=OntapApplicationTemplateSanApplicationComponentQosPolicy
    )


class OntapApplicationTemplateSanApplicationComponentStorageService(OntapModel):
    """OntapApplicationTemplateSanApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSanApplicationComponentTieringObjectStore(OntapModel):
    """OntapApplicationTemplateSanApplicationComponentTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapApplicationTemplateSanApplicationComponentTiering(OntapModel):
    """OntapApplicationTemplateSanApplicationComponentTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapApplicationTemplateSanApplicationComponentTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapApplicationTemplateSanApplicationComponent(OntapModel):
    """OntapApplicationTemplateSanApplicationComponent sub-model for application_components."""

    name: str = ""
    igroup_name: str = ""
    lun_count: int = 0
    os_type: str = ""
    qos: OntapApplicationTemplateSanApplicationComponentQos = Field(
        default_factory=OntapApplicationTemplateSanApplicationComponentQos
    )
    storage_service: OntapApplicationTemplateSanApplicationComponentStorageService = Field(
        default_factory=OntapApplicationTemplateSanApplicationComponentStorageService
    )
    tiering: OntapApplicationTemplateSanApplicationComponentTiering = Field(
        default_factory=OntapApplicationTemplateSanApplicationComponentTiering
    )
    total_size: int = 0


class OntapApplicationTemplateSanExcludeAggregate(OntapModel):
    """OntapApplicationTemplateSanExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateSanNewIgroup(OntapModel):
    """OntapApplicationTemplateSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationTemplateSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateSanProtectionType(OntapModel):
    """OntapApplicationTemplateSanProtectionType sub-model for protection_type."""

    local_policy: str = ""
    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateSan(OntapModel):
    """OntapApplicationTemplateSan sub-model for san."""

    application_components: list[OntapApplicationTemplateSanApplicationComponent] = Field(
        default_factory=list
    )
    exclude_aggregates: list[OntapApplicationTemplateSanExcludeAggregate] = Field(
        default_factory=list
    )
    new_igroups: list[OntapApplicationTemplateSanNewIgroup] = Field(default_factory=list)
    os_type: str = ""
    protection_type: OntapApplicationTemplateSanProtectionType = Field(
        default_factory=OntapApplicationTemplateSanProtectionType
    )


class OntapApplicationTemplateSqlOnSanDbStorageService(OntapModel):
    """OntapApplicationTemplateSqlOnSanDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSqlOnSanDb(OntapModel):
    """OntapApplicationTemplateSqlOnSanDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationTemplateSqlOnSanDbStorageService = Field(
        default_factory=OntapApplicationTemplateSqlOnSanDbStorageService
    )


class OntapApplicationTemplateSqlOnSanLogStorageService(OntapModel):
    """OntapApplicationTemplateSqlOnSanLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSqlOnSanLog(OntapModel):
    """OntapApplicationTemplateSqlOnSanLog sub-model for log."""

    size: int = 0
    storage_service: OntapApplicationTemplateSqlOnSanLogStorageService = Field(
        default_factory=OntapApplicationTemplateSqlOnSanLogStorageService
    )


class OntapApplicationTemplateSqlOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateSqlOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateSqlOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateSqlOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateSqlOnSanNewIgroup(OntapModel):
    """OntapApplicationTemplateSqlOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateSqlOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationTemplateSqlOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateSqlOnSanProtectionType(OntapModel):
    """OntapApplicationTemplateSqlOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateSqlOnSanTempDbStorageService(OntapModel):
    """OntapApplicationTemplateSqlOnSanTempDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSqlOnSanTempDb(OntapModel):
    """OntapApplicationTemplateSqlOnSanTempDb sub-model for temp_db."""

    size: int = 0
    storage_service: OntapApplicationTemplateSqlOnSanTempDbStorageService = Field(
        default_factory=OntapApplicationTemplateSqlOnSanTempDbStorageService
    )


class OntapApplicationTemplateSqlOnSan(OntapModel):
    """OntapApplicationTemplateSqlOnSan sub-model for sql_on_san."""

    db: OntapApplicationTemplateSqlOnSanDb = Field(
        default_factory=OntapApplicationTemplateSqlOnSanDb
    )
    igroup_name: str = ""
    log: OntapApplicationTemplateSqlOnSanLog = Field(
        default_factory=OntapApplicationTemplateSqlOnSanLog
    )
    new_igroups: list[OntapApplicationTemplateSqlOnSanNewIgroup] = Field(default_factory=list)
    os_type: str = ""
    protection_type: OntapApplicationTemplateSqlOnSanProtectionType = Field(
        default_factory=OntapApplicationTemplateSqlOnSanProtectionType
    )
    server_cores_count: int = 0
    temp_db: OntapApplicationTemplateSqlOnSanTempDb = Field(
        default_factory=OntapApplicationTemplateSqlOnSanTempDb
    )


class OntapApplicationTemplateSqlOnSmbAccess(OntapModel):
    """OntapApplicationTemplateSqlOnSmbAccess sub-model for access."""

    installer: str = ""
    service_account: str = ""


class OntapApplicationTemplateSqlOnSmbDbStorageService(OntapModel):
    """OntapApplicationTemplateSqlOnSmbDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSqlOnSmbDb(OntapModel):
    """OntapApplicationTemplateSqlOnSmbDb sub-model for db."""

    size: int = 0
    storage_service: OntapApplicationTemplateSqlOnSmbDbStorageService = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbDbStorageService
    )


class OntapApplicationTemplateSqlOnSmbLogStorageService(OntapModel):
    """OntapApplicationTemplateSqlOnSmbLogStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSqlOnSmbLog(OntapModel):
    """OntapApplicationTemplateSqlOnSmbLog sub-model for log."""

    size: int = 0
    storage_service: OntapApplicationTemplateSqlOnSmbLogStorageService = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbLogStorageService
    )


class OntapApplicationTemplateSqlOnSmbProtectionType(OntapModel):
    """OntapApplicationTemplateSqlOnSmbProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateSqlOnSmbTempDbStorageService(OntapModel):
    """OntapApplicationTemplateSqlOnSmbTempDbStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateSqlOnSmbTempDb(OntapModel):
    """OntapApplicationTemplateSqlOnSmbTempDb sub-model for temp_db."""

    size: int = 0
    storage_service: OntapApplicationTemplateSqlOnSmbTempDbStorageService = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbTempDbStorageService
    )


class OntapApplicationTemplateSqlOnSmb(OntapModel):
    """OntapApplicationTemplateSqlOnSmb sub-model for sql_on_smb."""

    access: OntapApplicationTemplateSqlOnSmbAccess = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbAccess
    )
    db: OntapApplicationTemplateSqlOnSmbDb = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbDb
    )
    log: OntapApplicationTemplateSqlOnSmbLog = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbLog
    )
    protection_type: OntapApplicationTemplateSqlOnSmbProtectionType = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbProtectionType
    )
    server_cores_count: int = 0
    temp_db: OntapApplicationTemplateSqlOnSmbTempDb = Field(
        default_factory=OntapApplicationTemplateSqlOnSmbTempDb
    )


class OntapApplicationTemplateVdiOnNasDesktopsStorageService(OntapModel):
    """OntapApplicationTemplateVdiOnNasDesktopsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateVdiOnNasDesktops(OntapModel):
    """OntapApplicationTemplateVdiOnNasDesktops sub-model for desktops."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateVdiOnNasDesktopsStorageService = Field(
        default_factory=OntapApplicationTemplateVdiOnNasDesktopsStorageService
    )


class OntapApplicationTemplateVdiOnNasHyperVAccess(OntapModel):
    """OntapApplicationTemplateVdiOnNasHyperVAccess sub-model for hyper_v_access."""

    service_account: str = ""


class OntapApplicationTemplateVdiOnNasNfsAccess(OntapModel):
    """OntapApplicationTemplateVdiOnNasNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateVdiOnNasProtectionType(OntapModel):
    """OntapApplicationTemplateVdiOnNasProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateVdiOnNas(OntapModel):
    """OntapApplicationTemplateVdiOnNas sub-model for vdi_on_nas."""

    desktops: OntapApplicationTemplateVdiOnNasDesktops = Field(
        default_factory=OntapApplicationTemplateVdiOnNasDesktops
    )
    hyper_v_access: OntapApplicationTemplateVdiOnNasHyperVAccess = Field(
        default_factory=OntapApplicationTemplateVdiOnNasHyperVAccess
    )
    nfs_access: list[OntapApplicationTemplateVdiOnNasNfsAccess] = Field(default_factory=list)
    protection_type: OntapApplicationTemplateVdiOnNasProtectionType = Field(
        default_factory=OntapApplicationTemplateVdiOnNasProtectionType
    )


class OntapApplicationTemplateVdiOnSanDesktopsStorageService(OntapModel):
    """OntapApplicationTemplateVdiOnSanDesktopsStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateVdiOnSanDesktops(OntapModel):
    """OntapApplicationTemplateVdiOnSanDesktops sub-model for desktops."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateVdiOnSanDesktopsStorageService = Field(
        default_factory=OntapApplicationTemplateVdiOnSanDesktopsStorageService
    )


class OntapApplicationTemplateVdiOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateVdiOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateVdiOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateVdiOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateVdiOnSanNewIgroup(OntapModel):
    """OntapApplicationTemplateVdiOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateVdiOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationTemplateVdiOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    protocol: str = ""


class OntapApplicationTemplateVdiOnSanProtectionType(OntapModel):
    """OntapApplicationTemplateVdiOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateVdiOnSan(OntapModel):
    """OntapApplicationTemplateVdiOnSan sub-model for vdi_on_san."""

    desktops: OntapApplicationTemplateVdiOnSanDesktops = Field(
        default_factory=OntapApplicationTemplateVdiOnSanDesktops
    )
    hypervisor: str = ""
    igroup_name: str = ""
    new_igroups: list[OntapApplicationTemplateVdiOnSanNewIgroup] = Field(default_factory=list)
    protection_type: OntapApplicationTemplateVdiOnSanProtectionType = Field(
        default_factory=OntapApplicationTemplateVdiOnSanProtectionType
    )


class OntapApplicationTemplateVsiOnNasDatastoreStorageService(OntapModel):
    """OntapApplicationTemplateVsiOnNasDatastoreStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateVsiOnNasDatastore(OntapModel):
    """OntapApplicationTemplateVsiOnNasDatastore sub-model for datastore."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateVsiOnNasDatastoreStorageService = Field(
        default_factory=OntapApplicationTemplateVsiOnNasDatastoreStorageService
    )


class OntapApplicationTemplateVsiOnNasHyperVAccess(OntapModel):
    """OntapApplicationTemplateVsiOnNasHyperVAccess sub-model for hyper_v_access."""

    service_account: str = ""


class OntapApplicationTemplateVsiOnNasNfsAccess(OntapModel):
    """OntapApplicationTemplateVsiOnNasNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateVsiOnNasProtectionType(OntapModel):
    """OntapApplicationTemplateVsiOnNasProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateVsiOnNas(OntapModel):
    """OntapApplicationTemplateVsiOnNas sub-model for vsi_on_nas."""

    datastore: OntapApplicationTemplateVsiOnNasDatastore = Field(
        default_factory=OntapApplicationTemplateVsiOnNasDatastore
    )
    hyper_v_access: OntapApplicationTemplateVsiOnNasHyperVAccess = Field(
        default_factory=OntapApplicationTemplateVsiOnNasHyperVAccess
    )
    nfs_access: list[OntapApplicationTemplateVsiOnNasNfsAccess] = Field(default_factory=list)
    protection_type: OntapApplicationTemplateVsiOnNasProtectionType = Field(
        default_factory=OntapApplicationTemplateVsiOnNasProtectionType
    )


class OntapApplicationTemplateVsiOnSanDatastoreStorageService(OntapModel):
    """OntapApplicationTemplateVsiOnSanDatastoreStorageService sub-model for storage_service."""

    name: str = ""


class OntapApplicationTemplateVsiOnSanDatastore(OntapModel):
    """OntapApplicationTemplateVsiOnSanDatastore sub-model for datastore."""

    count: int = 0
    size: int = 0
    storage_service: OntapApplicationTemplateVsiOnSanDatastoreStorageService = Field(
        default_factory=OntapApplicationTemplateVsiOnSanDatastoreStorageService
    )


class OntapApplicationTemplateVsiOnSanNewIgroupIgroup(OntapModel):
    """OntapApplicationTemplateVsiOnSanNewIgroupIgroup sub-model for igroups."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateVsiOnSanNewIgroupInitiatorObject(OntapModel):
    """OntapApplicationTemplateVsiOnSanNewIgroupInitiatorObject sub-model for initiator_objects."""

    name: str = ""
    comment: str = ""


class OntapApplicationTemplateVsiOnSanNewIgroup(OntapModel):
    """OntapApplicationTemplateVsiOnSanNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[OntapApplicationTemplateVsiOnSanNewIgroupIgroup] = Field(default_factory=list)
    initiator_objects: list[OntapApplicationTemplateVsiOnSanNewIgroupInitiatorObject] = Field(
        default_factory=list
    )
    initiators: list[str] = Field(default_factory=list)
    protocol: str = ""


class OntapApplicationTemplateVsiOnSanProtectionType(OntapModel):
    """OntapApplicationTemplateVsiOnSanProtectionType sub-model for protection_type."""

    local_rpo: str = ""
    remote_rpo: str = ""


class OntapApplicationTemplateVsiOnSan(OntapModel):
    """OntapApplicationTemplateVsiOnSan sub-model for vsi_on_san."""

    datastore: OntapApplicationTemplateVsiOnSanDatastore = Field(
        default_factory=OntapApplicationTemplateVsiOnSanDatastore
    )
    hypervisor: str = ""
    igroup_name: str = ""
    new_igroups: list[OntapApplicationTemplateVsiOnSanNewIgroup] = Field(default_factory=list)
    protection_type: OntapApplicationTemplateVsiOnSanProtectionType = Field(
        default_factory=OntapApplicationTemplateVsiOnSanProtectionType
    )


class OntapApplicationTemplate(OntapModel):
    """OntapApplicationTemplate information."""

    name: str = ""
    description: str = ""
    missing_prerequisites: str = ""
    mongo_db_on_san: OntapApplicationTemplateMongoDbOnSan = Field(
        default_factory=OntapApplicationTemplateMongoDbOnSan
    )
    nas: OntapApplicationTemplateNas = Field(default_factory=OntapApplicationTemplateNas)
    nvme: OntapApplicationTemplateNvme = Field(default_factory=OntapApplicationTemplateNvme)
    oracle_on_nfs: OntapApplicationTemplateOracleOnNfs = Field(
        default_factory=OntapApplicationTemplateOracleOnNfs
    )
    oracle_on_san: OntapApplicationTemplateOracleOnSan = Field(
        default_factory=OntapApplicationTemplateOracleOnSan
    )
    oracle_rac_on_nfs: OntapApplicationTemplateOracleRacOnNfs = Field(
        default_factory=OntapApplicationTemplateOracleRacOnNfs
    )
    oracle_rac_on_san: OntapApplicationTemplateOracleRacOnSan = Field(
        default_factory=OntapApplicationTemplateOracleRacOnSan
    )
    protocol: str = ""
    s3_bucket: OntapApplicationTemplateS3Bucket = Field(
        default_factory=OntapApplicationTemplateS3Bucket
    )
    san: OntapApplicationTemplateSan = Field(default_factory=OntapApplicationTemplateSan)
    sql_on_san: OntapApplicationTemplateSqlOnSan = Field(
        default_factory=OntapApplicationTemplateSqlOnSan
    )
    sql_on_smb: OntapApplicationTemplateSqlOnSmb = Field(
        default_factory=OntapApplicationTemplateSqlOnSmb
    )
    vdi_on_nas: OntapApplicationTemplateVdiOnNas = Field(
        default_factory=OntapApplicationTemplateVdiOnNas
    )
    vdi_on_san: OntapApplicationTemplateVdiOnSan = Field(
        default_factory=OntapApplicationTemplateVdiOnSan
    )
    vsi_on_nas: OntapApplicationTemplateVsiOnNas = Field(
        default_factory=OntapApplicationTemplateVsiOnNas
    )
    vsi_on_san: OntapApplicationTemplateVsiOnSan = Field(
        default_factory=OntapApplicationTemplateVsiOnSan
    )
