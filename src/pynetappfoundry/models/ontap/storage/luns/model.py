"""OntapLun information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLunAttribute(OntapModel):
    """OntapLunAttribute sub-model for attributes."""

    name: str = ""
    value: str = ""


class OntapLunCloneSource(OntapModel):
    """OntapLunCloneSource sub-model for source."""

    name: str = ""
    uuid: str = ""


class OntapLunClone(OntapModel):
    """OntapLunClone sub-model for clone."""

    source: OntapLunCloneSource = Field(default_factory=OntapLunCloneSource)


class OntapLunConsistencyGroup(OntapModel):
    """OntapLunConsistencyGroup sub-model for consistency_group."""

    name: str = ""
    uuid: str = ""


class OntapLunConvertNamespace(OntapModel):
    """OntapLunConvertNamespace sub-model for namespace."""

    name: str = ""
    uuid: str = ""


class OntapLunConvert(OntapModel):
    """OntapLunConvert sub-model for convert."""

    namespace: OntapLunConvertNamespace = Field(default_factory=OntapLunConvertNamespace)


class OntapLunCopyDestinationPeer(OntapModel):
    """OntapLunCopyDestinationPeer sub-model for peer."""

    name: str = ""
    uuid: str = ""


class OntapLunCopyDestinationProgressFailureArgument(OntapModel):
    """OntapLunCopyDestinationProgressFailureArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapLunCopyDestinationProgressFailure(OntapModel):
    """OntapLunCopyDestinationProgressFailure sub-model for failure."""

    arguments: list[OntapLunCopyDestinationProgressFailureArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapLunCopyDestinationProgress(OntapModel):
    """OntapLunCopyDestinationProgress sub-model for progress."""

    elapsed: int = 0
    failure: OntapLunCopyDestinationProgressFailure = Field(
        default_factory=OntapLunCopyDestinationProgressFailure
    )
    percent_complete: int = 0
    state: str = ""
    volume_snapshot_blocked: bool = False


class OntapLunCopyDestination(OntapModel):
    """OntapLunCopyDestination sub-model for destinations."""

    max_throughput: int = 0
    name: str = ""
    peer: OntapLunCopyDestinationPeer = Field(default_factory=OntapLunCopyDestinationPeer)
    progress: OntapLunCopyDestinationProgress = Field(
        default_factory=OntapLunCopyDestinationProgress
    )
    uuid: str = ""


class OntapLunCopySourcePeer(OntapModel):
    """OntapLunCopySourcePeer sub-model for peer."""

    name: str = ""
    uuid: str = ""


class OntapLunCopySourceProgressFailureArgument(OntapModel):
    """OntapLunCopySourceProgressFailureArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapLunCopySourceProgressFailure(OntapModel):
    """OntapLunCopySourceProgressFailure sub-model for failure."""

    arguments: list[OntapLunCopySourceProgressFailureArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapLunCopySourceProgress(OntapModel):
    """OntapLunCopySourceProgress sub-model for progress."""

    elapsed: int = 0
    failure: OntapLunCopySourceProgressFailure = Field(
        default_factory=OntapLunCopySourceProgressFailure
    )
    percent_complete: int = 0
    state: str = ""
    volume_snapshot_blocked: bool = False


class OntapLunCopySource(OntapModel):
    """OntapLunCopySource sub-model for source."""

    max_throughput: int = 0
    name: str = ""
    peer: OntapLunCopySourcePeer = Field(default_factory=OntapLunCopySourcePeer)
    progress: OntapLunCopySourceProgress = Field(default_factory=OntapLunCopySourceProgress)
    uuid: str = ""


class OntapLunCopy(OntapModel):
    """OntapLunCopy sub-model for copy."""

    destinations: list[OntapLunCopyDestination] = Field(default_factory=list)
    source: OntapLunCopySource = Field(default_factory=OntapLunCopySource)


class OntapLunLocationNode(OntapModel):
    """OntapLunLocationNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapLunLocationQtree(OntapModel):
    """OntapLunLocationQtree sub-model for qtree."""

    id: int = 0
    name: str = ""


class OntapLunLocationVolume(OntapModel):
    """OntapLunLocationVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapLunLocation(OntapModel):
    """OntapLunLocation sub-model for location."""

    logical_unit: str = ""
    node: OntapLunLocationNode = Field(default_factory=OntapLunLocationNode)
    qtree: OntapLunLocationQtree = Field(default_factory=OntapLunLocationQtree)
    volume: OntapLunLocationVolume = Field(default_factory=OntapLunLocationVolume)


class OntapLunLunMapIgroupIgroup(OntapModel):
    """OntapLunLunMapIgroupIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapLunLunMapIgroupInitiator(OntapModel):
    """OntapLunLunMapIgroupInitiator sub-model for initiators."""

    comment: str = ""
    name: str = ""


class OntapLunLunMapIgroup(OntapModel):
    """OntapLunLunMapIgroup sub-model for igroup."""

    comment: str = ""
    igroups: list[OntapLunLunMapIgroupIgroup] = Field(default_factory=list)
    initiators: list[OntapLunLunMapIgroupInitiator] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    protocol: str = ""
    uuid: str = ""


class OntapLunLunMap(OntapModel):
    """OntapLunLunMap sub-model for lun_maps."""

    igroup: OntapLunLunMapIgroup = Field(default_factory=OntapLunLunMapIgroup)
    logical_unit_number: int = 0


class OntapLunMetricIops(OntapModel):
    """OntapLunMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapLunMetricLatency(OntapModel):
    """OntapLunMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapLunMetricThroughput(OntapModel):
    """OntapLunMetricThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapLunMetric(OntapModel):
    """OntapLunMetric sub-model for metric."""

    duration: str = ""
    iops: OntapLunMetricIops = Field(default_factory=OntapLunMetricIops)
    latency: OntapLunMetricLatency = Field(default_factory=OntapLunMetricLatency)
    status: str = ""
    throughput: OntapLunMetricThroughput = Field(default_factory=OntapLunMetricThroughput)
    timestamp: str = ""


class OntapLunMovementPaths(OntapModel):
    """OntapLunMovementPaths sub-model for paths."""

    destination: str = ""
    source: str = ""


class OntapLunMovementProgressFailureArgument(OntapModel):
    """OntapLunMovementProgressFailureArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapLunMovementProgressFailure(OntapModel):
    """OntapLunMovementProgressFailure sub-model for failure."""

    arguments: list[OntapLunMovementProgressFailureArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapLunMovementProgress(OntapModel):
    """OntapLunMovementProgress sub-model for progress."""

    elapsed: int = 0
    failure: OntapLunMovementProgressFailure = Field(
        default_factory=OntapLunMovementProgressFailure
    )
    percent_complete: int = 0
    state: str = ""
    volume_snapshot_blocked: bool = False


class OntapLunMovement(OntapModel):
    """OntapLunMovement sub-model for movement."""

    max_throughput: int = 0
    paths: OntapLunMovementPaths = Field(default_factory=OntapLunMovementPaths)
    progress: OntapLunMovementProgress = Field(default_factory=OntapLunMovementProgress)


class OntapLunProvisioningOptionsQosPolicy(OntapModel):
    """OntapLunProvisioningOptionsQosPolicy sub-model for qos_policy."""

    name: str = ""
    uuid: str = ""


class OntapLunProvisioningOptionsSnapshotPolicy(OntapModel):
    """OntapLunProvisioningOptionsSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapLunProvisioningOptionsStorageService(OntapModel):
    """OntapLunProvisioningOptionsStorageService sub-model for storage_service."""

    name: str = ""


class OntapLunProvisioningOptionsTieringObjectStore(OntapModel):
    """OntapLunProvisioningOptionsTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapLunProvisioningOptionsTiering(OntapModel):
    """OntapLunProvisioningOptionsTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapLunProvisioningOptionsTieringObjectStore] = Field(default_factory=list)
    policy: str = ""


class OntapLunProvisioningOptions(OntapModel):
    """OntapLunProvisioningOptions sub-model for provisioning_options."""

    auto: bool = False
    count: int = 0
    qos_policy: OntapLunProvisioningOptionsQosPolicy = Field(
        default_factory=OntapLunProvisioningOptionsQosPolicy
    )
    snapshot_policy: OntapLunProvisioningOptionsSnapshotPolicy = Field(
        default_factory=OntapLunProvisioningOptionsSnapshotPolicy
    )
    storage_service: OntapLunProvisioningOptionsStorageService = Field(
        default_factory=OntapLunProvisioningOptionsStorageService
    )
    tiering: OntapLunProvisioningOptionsTiering = Field(
        default_factory=OntapLunProvisioningOptionsTiering
    )
    use_mirrored_aggregates: bool = False


class OntapLunQosPolicy(OntapModel):
    """OntapLunQosPolicy sub-model for qos_policy."""

    name: str = ""
    uuid: str = ""


class OntapLunSpaceGuarantee(OntapModel):
    """OntapLunSpaceGuarantee sub-model for guarantee."""

    requested: bool = False
    reserved: bool = False


class OntapLunSpace(OntapModel):
    """OntapLunSpace sub-model for space."""

    efficiency_ratio: float = 0.0
    guarantee: OntapLunSpaceGuarantee = Field(default_factory=OntapLunSpaceGuarantee)
    physical_used: int = 0
    physical_used_by_snapshots: int = 0
    scsi_thin_provisioning_support_enabled: bool = False
    size: int = 0
    used: int = 0


class OntapLunStatisticsIopsRaw(OntapModel):
    """OntapLunStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapLunStatisticsLatencyRaw(OntapModel):
    """OntapLunStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapLunStatisticsThroughputRaw(OntapModel):
    """OntapLunStatisticsThroughputRaw sub-model for throughput_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapLunStatistics(OntapModel):
    """OntapLunStatistics sub-model for statistics."""

    iops_raw: OntapLunStatisticsIopsRaw = Field(default_factory=OntapLunStatisticsIopsRaw)
    latency_raw: OntapLunStatisticsLatencyRaw = Field(default_factory=OntapLunStatisticsLatencyRaw)
    status: str = ""
    throughput_raw: OntapLunStatisticsThroughputRaw = Field(
        default_factory=OntapLunStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapLunStatus(OntapModel):
    """OntapLunStatus sub-model for status."""

    container_state: str = ""
    mapped: bool = False
    read_only: bool = False
    state: str = ""


class OntapLunSvm(OntapModel):
    """OntapLunSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapLunVvolBindingPartner(OntapModel):
    """OntapLunVvolBindingPartner sub-model for partner."""

    name: str = ""
    uuid: str = ""


class OntapLunVvolBinding(OntapModel):
    """OntapLunVvolBinding sub-model for bindings."""

    id: int = 0
    partner: OntapLunVvolBindingPartner = Field(default_factory=OntapLunVvolBindingPartner)
    secondary_id: str = ""


class OntapLunVvol(OntapModel):
    """OntapLunVvol sub-model for vvol."""

    bindings: list[OntapLunVvolBinding] = Field(default_factory=list)
    is_bound: bool = False


class OntapLun(OntapModel):
    """OntapLun information."""

    attributes: list[OntapLunAttribute] = Field(default_factory=list)
    auto_delete: bool = False
    class_: str = ""
    clone: OntapLunClone = Field(default_factory=OntapLunClone)
    comment: str = ""
    consistency_group: OntapLunConsistencyGroup = Field(default_factory=OntapLunConsistencyGroup)
    convert: OntapLunConvert = Field(default_factory=OntapLunConvert)
    copy_: OntapLunCopy = Field(default_factory=OntapLunCopy)
    create_time: str = ""
    enabled: bool = False
    location: OntapLunLocation = Field(default_factory=OntapLunLocation)
    lun_maps: list[OntapLunLunMap] = Field(default_factory=list)
    metric: OntapLunMetric = Field(default_factory=OntapLunMetric)
    movement: OntapLunMovement = Field(default_factory=OntapLunMovement)
    name: str = ""
    os_type: str = ""
    provisioning_options: OntapLunProvisioningOptions = Field(
        default_factory=OntapLunProvisioningOptions
    )
    qos_policy: OntapLunQosPolicy = Field(default_factory=OntapLunQosPolicy)
    serial_number: str = ""
    space: OntapLunSpace = Field(default_factory=OntapLunSpace)
    statistics: OntapLunStatistics = Field(default_factory=OntapLunStatistics)
    status: OntapLunStatus = Field(default_factory=OntapLunStatus)
    svm: OntapLunSvm = Field(default_factory=OntapLunSvm)
    uuid: str = ""
    vvol: OntapLunVvol = Field(default_factory=OntapLunVvol)
