"""OntapNvmeNamespace information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeNamespaceCloneSource(OntapModel):
    """OntapNvmeNamespaceCloneSource sub-model for source."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceClone(OntapModel):
    """OntapNvmeNamespaceClone sub-model for clone."""

    source: OntapNvmeNamespaceCloneSource = Field(default_factory=OntapNvmeNamespaceCloneSource)


class OntapNvmeNamespaceConsistencyGroup(OntapModel):
    """OntapNvmeNamespaceConsistencyGroup sub-model for consistency_group."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceConvertLun(OntapModel):
    """OntapNvmeNamespaceConvertLun sub-model for lun."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceConvert(OntapModel):
    """OntapNvmeNamespaceConvert sub-model for convert."""

    lun: OntapNvmeNamespaceConvertLun = Field(default_factory=OntapNvmeNamespaceConvertLun)


class OntapNvmeNamespaceLocationNode(OntapModel):
    """OntapNvmeNamespaceLocationNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceLocationQtree(OntapModel):
    """OntapNvmeNamespaceLocationQtree sub-model for qtree."""

    id: int = 0
    name: str = ""


class OntapNvmeNamespaceLocationVolume(OntapModel):
    """OntapNvmeNamespaceLocationVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceLocation(OntapModel):
    """OntapNvmeNamespaceLocation sub-model for location."""

    namespace: str = ""
    node: OntapNvmeNamespaceLocationNode = Field(default_factory=OntapNvmeNamespaceLocationNode)
    qtree: OntapNvmeNamespaceLocationQtree = Field(default_factory=OntapNvmeNamespaceLocationQtree)
    volume: OntapNvmeNamespaceLocationVolume = Field(
        default_factory=OntapNvmeNamespaceLocationVolume
    )


class OntapNvmeNamespaceMetricIops(OntapModel):
    """OntapNvmeNamespaceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeNamespaceMetricLatency(OntapModel):
    """OntapNvmeNamespaceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeNamespaceMetricThroughput(OntapModel):
    """OntapNvmeNamespaceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeNamespaceMetric(OntapModel):
    """OntapNvmeNamespaceMetric sub-model for metric."""

    duration: str = ""
    iops: OntapNvmeNamespaceMetricIops = Field(default_factory=OntapNvmeNamespaceMetricIops)
    latency: OntapNvmeNamespaceMetricLatency = Field(
        default_factory=OntapNvmeNamespaceMetricLatency
    )
    status: str = ""
    throughput: OntapNvmeNamespaceMetricThroughput = Field(
        default_factory=OntapNvmeNamespaceMetricThroughput
    )
    timestamp: str = ""


class OntapNvmeNamespaceProvisioningOptionsQosPolicy(OntapModel):
    """OntapNvmeNamespaceProvisioningOptionsQosPolicy sub-model for qos_policy."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceProvisioningOptionsSnapshotPolicy(OntapModel):
    """OntapNvmeNamespaceProvisioningOptionsSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespaceProvisioningOptionsStorageService(OntapModel):
    """OntapNvmeNamespaceProvisioningOptionsStorageService sub-model for storage_service."""

    name: str = ""


class OntapNvmeNamespaceProvisioningOptionsTieringObjectStore(OntapModel):
    """OntapNvmeNamespaceProvisioningOptionsTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapNvmeNamespaceProvisioningOptionsTiering(OntapModel):
    """OntapNvmeNamespaceProvisioningOptionsTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapNvmeNamespaceProvisioningOptionsTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapNvmeNamespaceProvisioningOptions(OntapModel):
    """OntapNvmeNamespaceProvisioningOptions sub-model for provisioning_options."""

    auto: bool = False
    count: int = 0
    qos_policy: OntapNvmeNamespaceProvisioningOptionsQosPolicy = Field(
        default_factory=OntapNvmeNamespaceProvisioningOptionsQosPolicy
    )
    snapshot_policy: OntapNvmeNamespaceProvisioningOptionsSnapshotPolicy = Field(
        default_factory=OntapNvmeNamespaceProvisioningOptionsSnapshotPolicy
    )
    storage_service: OntapNvmeNamespaceProvisioningOptionsStorageService = Field(
        default_factory=OntapNvmeNamespaceProvisioningOptionsStorageService
    )
    tiering: OntapNvmeNamespaceProvisioningOptionsTiering = Field(
        default_factory=OntapNvmeNamespaceProvisioningOptionsTiering
    )
    use_mirrored_aggregates: bool = False


class OntapNvmeNamespaceSpaceGuarantee(OntapModel):
    """OntapNvmeNamespaceSpaceGuarantee sub-model for guarantee."""

    requested: bool = False
    reserved: bool = False


class OntapNvmeNamespaceSpace(OntapModel):
    """OntapNvmeNamespaceSpace sub-model for space."""

    block_size: int = 0
    efficiency_ratio: float = 0.0
    guarantee: OntapNvmeNamespaceSpaceGuarantee = Field(
        default_factory=OntapNvmeNamespaceSpaceGuarantee
    )
    physical_used: int = 0
    physical_used_by_snapshots: int = 0
    size: int = 0
    used: int = 0


class OntapNvmeNamespaceStatisticsIopsRaw(OntapModel):
    """OntapNvmeNamespaceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeNamespaceStatisticsLatencyRaw(OntapModel):
    """OntapNvmeNamespaceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeNamespaceStatisticsThroughputRaw(OntapModel):
    """OntapNvmeNamespaceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeNamespaceStatistics(OntapModel):
    """OntapNvmeNamespaceStatistics sub-model for statistics."""

    iops_raw: OntapNvmeNamespaceStatisticsIopsRaw = Field(
        default_factory=OntapNvmeNamespaceStatisticsIopsRaw
    )
    latency_raw: OntapNvmeNamespaceStatisticsLatencyRaw = Field(
        default_factory=OntapNvmeNamespaceStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapNvmeNamespaceStatisticsThroughputRaw = Field(
        default_factory=OntapNvmeNamespaceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapNvmeNamespaceStatus(OntapModel):
    """OntapNvmeNamespaceStatus sub-model for status."""

    container_state: str = ""
    mapped: bool = False
    read_only: bool = False
    state: str = ""


class OntapNvmeNamespaceSubsystemMapSubsystemHostDhHmacChap(OntapModel):
    """OntapNvmeNamespaceSubsystemMapSubsystemHostDhHmacChap sub-model for dh_hmac_chap."""

    controller_secret_key: str = ""
    group_size: str = ""
    hash_function: str = ""
    host_secret_key: str = ""
    mode: str = ""


class OntapNvmeNamespaceSubsystemMapSubsystemHostTls(OntapModel):
    """OntapNvmeNamespaceSubsystemMapSubsystemHostTls sub-model for tls."""

    configured_psk: str = ""
    key_type: str = ""


class OntapNvmeNamespaceSubsystemMapSubsystemHost(OntapModel):
    """OntapNvmeNamespaceSubsystemMapSubsystemHost sub-model for hosts."""

    dh_hmac_chap: OntapNvmeNamespaceSubsystemMapSubsystemHostDhHmacChap = Field(
        default_factory=OntapNvmeNamespaceSubsystemMapSubsystemHostDhHmacChap
    )
    nqn: str = ""
    priority: str = ""
    tls: OntapNvmeNamespaceSubsystemMapSubsystemHostTls = Field(
        default_factory=OntapNvmeNamespaceSubsystemMapSubsystemHostTls
    )


class OntapNvmeNamespaceSubsystemMapSubsystem(OntapModel):
    """OntapNvmeNamespaceSubsystemMapSubsystem sub-model for subsystem."""

    comment: str = ""
    hosts: list[OntapNvmeNamespaceSubsystemMapSubsystemHost] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    uuid: str = ""


class OntapNvmeNamespaceSubsystemMap(OntapModel):
    """OntapNvmeNamespaceSubsystemMap sub-model for subsystem_map."""

    anagrpid: str = ""
    nsid: str = ""
    subsystem: OntapNvmeNamespaceSubsystemMapSubsystem = Field(
        default_factory=OntapNvmeNamespaceSubsystemMapSubsystem
    )


class OntapNvmeNamespaceSvm(OntapModel):
    """OntapNvmeNamespaceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNvmeNamespace(OntapModel):
    """OntapNvmeNamespace information."""

    auto_delete: bool = False
    clone: OntapNvmeNamespaceClone = Field(default_factory=OntapNvmeNamespaceClone)
    comment: str = ""
    consistency_group: OntapNvmeNamespaceConsistencyGroup = Field(
        default_factory=OntapNvmeNamespaceConsistencyGroup
    )
    convert: OntapNvmeNamespaceConvert = Field(default_factory=OntapNvmeNamespaceConvert)
    create_time: str = ""
    enabled: bool = False
    location: OntapNvmeNamespaceLocation = Field(default_factory=OntapNvmeNamespaceLocation)
    metric: OntapNvmeNamespaceMetric = Field(default_factory=OntapNvmeNamespaceMetric)
    name: str = ""
    os_type: str = ""
    provisioning_options: OntapNvmeNamespaceProvisioningOptions = Field(
        default_factory=OntapNvmeNamespaceProvisioningOptions
    )
    space: OntapNvmeNamespaceSpace = Field(default_factory=OntapNvmeNamespaceSpace)
    statistics: OntapNvmeNamespaceStatistics = Field(default_factory=OntapNvmeNamespaceStatistics)
    status: OntapNvmeNamespaceStatus = Field(default_factory=OntapNvmeNamespaceStatus)
    subsystem_map: OntapNvmeNamespaceSubsystemMap = Field(
        default_factory=OntapNvmeNamespaceSubsystemMap
    )
    svm: OntapNvmeNamespaceSvm = Field(default_factory=OntapNvmeNamespaceSvm)
    uuid: str = ""
