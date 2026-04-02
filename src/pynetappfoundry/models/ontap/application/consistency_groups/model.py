# ruff: noqa: E501
"""OntapConsistencyGroupResponse information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupResponseApplication(OntapModel):
    """OntapConsistencyGroupResponseApplication sub-model for application."""

    component_type: str = ""
    type_: str = ""


class OntapConsistencyGroupResponseCloneGuarantee(OntapModel):
    """OntapConsistencyGroupResponseCloneGuarantee sub-model for guarantee."""

    type_: str = ""


class OntapConsistencyGroupResponseCloneParentConsistencyGroup(OntapModel):
    """OntapConsistencyGroupResponseCloneParentConsistencyGroup sub-model for parent_consistency_group."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseCloneParentSnapshot(OntapModel):
    """OntapConsistencyGroupResponseCloneParentSnapshot sub-model for parent_snapshot."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseCloneParentSvm(OntapModel):
    """OntapConsistencyGroupResponseCloneParentSvm sub-model for parent_svm."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseCloneVolume(OntapModel):
    """OntapConsistencyGroupResponseCloneVolume sub-model for volume."""

    prefix: str = ""
    suffix: str = ""


class OntapConsistencyGroupResponseClone(OntapModel):
    """OntapConsistencyGroupResponseClone sub-model for clone."""

    guarantee: OntapConsistencyGroupResponseCloneGuarantee = Field(
        default_factory=OntapConsistencyGroupResponseCloneGuarantee
    )
    is_flexclone: bool = False
    parent_consistency_group: OntapConsistencyGroupResponseCloneParentConsistencyGroup = Field(
        default_factory=OntapConsistencyGroupResponseCloneParentConsistencyGroup
    )
    parent_snapshot: OntapConsistencyGroupResponseCloneParentSnapshot = Field(
        default_factory=OntapConsistencyGroupResponseCloneParentSnapshot
    )
    parent_svm: OntapConsistencyGroupResponseCloneParentSvm = Field(
        default_factory=OntapConsistencyGroupResponseCloneParentSvm
    )
    split_complete_percent: int = 0
    split_estimate: int = 0
    split_initiated: bool = False
    volume: OntapConsistencyGroupResponseCloneVolume = Field(
        default_factory=OntapConsistencyGroupResponseCloneVolume
    )


class OntapConsistencyGroupResponseConsistencyGroupApplication(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupApplication sub-model for application."""

    component_type: str = ""
    type_: str = ""


class OntapConsistencyGroupResponseConsistencyGroupLunCloneSource(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunCloneSource sub-model for source."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupLunClone(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunClone sub-model for clone."""

    source: OntapConsistencyGroupResponseConsistencyGroupLunCloneSource = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunCloneSource
    )


class OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroupIgroup(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroupIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroupInitiator(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroupInitiator sub-model for initiators."""

    comment: str = ""
    name: str = ""


class OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroup(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroup sub-model for igroup."""

    comment: str = ""
    igroups: list[OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroupIgroup] = Field(
        default_factory=list
    )
    initiators: list[OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroupInitiator] = Field(
        default_factory=list
    )
    name: str = ""
    os_type: str = ""
    protocol: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupLunLunMap(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunLunMap sub-model for lun_maps."""

    igroup: OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroup = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunLunMapIgroup
    )
    logical_unit_number: int = 0


class OntapConsistencyGroupResponseConsistencyGroupLunProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    count: int = 0


class OntapConsistencyGroupResponseConsistencyGroupLunQosPolicy(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunQosPolicy sub-model for policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupLunQos(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunQos sub-model for qos."""

    policy: OntapConsistencyGroupResponseConsistencyGroupLunQosPolicy = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunQosPolicy
    )


class OntapConsistencyGroupResponseConsistencyGroupLunSpaceGuarantee(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunSpaceGuarantee sub-model for guarantee."""

    requested: bool = False
    reserved: bool = False


class OntapConsistencyGroupResponseConsistencyGroupLunSpace(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLunSpace sub-model for space."""

    guarantee: OntapConsistencyGroupResponseConsistencyGroupLunSpaceGuarantee = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunSpaceGuarantee
    )
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseConsistencyGroupLun(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupLun sub-model for luns."""

    clone: OntapConsistencyGroupResponseConsistencyGroupLunClone = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunClone
    )
    comment: str = ""
    create_time: str = ""
    enabled: bool = False
    lun_maps: list[OntapConsistencyGroupResponseConsistencyGroupLunLunMap] = Field(
        default_factory=list
    )
    name: str = ""
    os_type: str = ""
    provisioning_options: OntapConsistencyGroupResponseConsistencyGroupLunProvisioningOptions = (
        Field(default_factory=OntapConsistencyGroupResponseConsistencyGroupLunProvisioningOptions)
    )
    qos: OntapConsistencyGroupResponseConsistencyGroupLunQos = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunQos
    )
    serial_number: str = ""
    space: OntapConsistencyGroupResponseConsistencyGroupLunSpace = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupLunSpace
    )
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupNamespaceProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    count: int = 0


class OntapConsistencyGroupResponseConsistencyGroupNamespaceSpaceGuarantee(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceSpaceGuarantee sub-model for guarantee."""

    requested: bool = False
    reserved: bool = False


class OntapConsistencyGroupResponseConsistencyGroupNamespaceSpace(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceSpace sub-model for space."""

    block_size: int = 0
    guarantee: OntapConsistencyGroupResponseConsistencyGroupNamespaceSpaceGuarantee = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupNamespaceSpaceGuarantee
    )
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseConsistencyGroupNamespaceStatus(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceStatus sub-model for status."""

    container_state: str = ""
    mapped: bool = False
    read_only: bool = False
    state: str = ""


class OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystemHost(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystemHost sub-model for hosts."""

    nqn: str = ""
    priority: str = ""


class OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystem(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystem sub-model for subsystem."""

    comment: str = ""
    hosts: list[OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystemHost] = (
        Field(default_factory=list)
    )
    name: str = ""
    os_type: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMap(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMap sub-model for subsystem_map."""

    anagrpid: str = ""
    nsid: str = ""
    subsystem: OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystem = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMapSubsystem
    )


class OntapConsistencyGroupResponseConsistencyGroupNamespace(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupNamespace sub-model for namespaces."""

    auto_delete: bool = False
    comment: str = ""
    create_time: str = ""
    enabled: bool = False
    name: str = ""
    os_type: str = ""
    provisioning_options: OntapConsistencyGroupResponseConsistencyGroupNamespaceProvisioningOptions = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupNamespaceProvisioningOptions
    )
    space: OntapConsistencyGroupResponseConsistencyGroupNamespaceSpace = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupNamespaceSpace
    )
    status: OntapConsistencyGroupResponseConsistencyGroupNamespaceStatus = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupNamespaceStatus
    )
    subsystem_map: OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMap = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupNamespaceSubsystemMap
    )
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupParentConsistencyGroup(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupParentConsistencyGroup sub-model for parent_consistency_group."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupProvisioningOptionsStorageService(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupProvisioningOptionsStorageService sub-model for storage_service."""

    name: str = ""


class OntapConsistencyGroupResponseConsistencyGroupProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    name: str = ""
    storage_service: OntapConsistencyGroupResponseConsistencyGroupProvisioningOptionsStorageService = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupProvisioningOptionsStorageService
    )


class OntapConsistencyGroupResponseConsistencyGroupQosPolicy(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupQosPolicy sub-model for policy."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupQos(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupQos sub-model for qos."""

    policy: OntapConsistencyGroupResponseConsistencyGroupQosPolicy = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupQosPolicy
    )


class OntapConsistencyGroupResponseConsistencyGroupRestoreToSnapshot(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupRestoreToSnapshot sub-model for snapshot."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupRestoreTo(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupRestoreTo sub-model for restore_to."""

    snapshot: OntapConsistencyGroupResponseConsistencyGroupRestoreToSnapshot = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupRestoreToSnapshot
    )


class OntapConsistencyGroupResponseConsistencyGroupSnapshotPolicy(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupSpace(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupSpace sub-model for space."""

    available: int = 0
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseConsistencyGroupSvm(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupTieringObjectStore(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapConsistencyGroupResponseConsistencyGroupTiering(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapConsistencyGroupResponseConsistencyGroupTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifsShare(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifsShare sub-model for shares."""

    access_based_enumeration: bool = False
    acls: list[dict[str, Any]] = Field(default_factory=list)
    allow_unencrypted_access: bool = False
    change_notify: bool = False
    comment: str = ""
    continuously_available: bool = False
    dir_umask: int = 0
    encryption: bool = False
    file_umask: int = 0
    home_directory: bool = False
    name: str = ""
    namespace_caching: bool = False
    no_strict_security: bool = False
    offline_files: str = ""
    oplocks: bool = False
    show_snapshot: bool = False
    unix_symlink: str = ""
    vscan_profile: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifs(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifs sub-model for cifs."""

    shares: list[OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifsShare] = Field(
        default_factory=list
    )


class OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicyRule(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicyRule sub-model for rules."""

    allow_device_creation: bool = False
    allow_suid: bool = False
    anonymous_user: str = ""
    chown_mode: str = ""
    clients: list[dict[str, Any]] = Field(default_factory=list)
    index: int = 0
    ntfs_unix_security: str = ""
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)


class OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicy(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicy sub-model for export_policy."""

    id: int = 0
    name: str = ""
    rules: list[OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicyRule] = Field(
        default_factory=list
    )


class OntapConsistencyGroupResponseConsistencyGroupVolumeNasJunctionParent(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeNasJunctionParent sub-model for junction_parent."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolumeNas(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeNas sub-model for nas."""

    cifs: OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifs = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeNasCifs
    )
    export_policy: OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicy = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeNasExportPolicy
    )
    gid: int = 0
    junction_parent: OntapConsistencyGroupResponseConsistencyGroupVolumeNasJunctionParent = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeNasJunctionParent
    )
    path: str = ""
    security_style: str = ""
    uid: int = 0
    unix_permissions: int = 0


class OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptionsStorageService(
    OntapModel
):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptionsStorageService sub-model for storage_service."""

    name: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    count: int = 0
    storage_service: OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptionsStorageService = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptionsStorageService
    )


class OntapConsistencyGroupResponseConsistencyGroupVolumeQosPolicy(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeQosPolicy sub-model for policy."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolumeQos(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeQos sub-model for qos."""

    policy: OntapConsistencyGroupResponseConsistencyGroupVolumeQosPolicy = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeQosPolicy
    )


class OntapConsistencyGroupResponseConsistencyGroupVolumeSpace(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeSpace sub-model for space."""

    available: int = 0
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseConsistencyGroupVolumeTieringObjectStore(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolumeTiering(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolumeTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapConsistencyGroupResponseConsistencyGroupVolumeTieringObjectStore] = (
        Field(default_factory=list)
    )
    policy: str = ""


class OntapConsistencyGroupResponseConsistencyGroupVolume(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroupVolume sub-model for volumes."""

    comment: str = ""
    name: str = ""
    nas: OntapConsistencyGroupResponseConsistencyGroupVolumeNas = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeNas
    )
    provisioning_options: OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptions = (
        Field(
            default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeProvisioningOptions
        )
    )
    qos: OntapConsistencyGroupResponseConsistencyGroupVolumeQos = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeQos
    )
    space: OntapConsistencyGroupResponseConsistencyGroupVolumeSpace = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeSpace
    )
    tiering: OntapConsistencyGroupResponseConsistencyGroupVolumeTiering = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupVolumeTiering
    )
    uuid: str = ""


class OntapConsistencyGroupResponseConsistencyGroup(OntapModel):
    """OntapConsistencyGroupResponseConsistencyGroup sub-model for consistency_groups."""

    application: OntapConsistencyGroupResponseConsistencyGroupApplication = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupApplication
    )
    luns: list[OntapConsistencyGroupResponseConsistencyGroupLun] = Field(default_factory=list)
    name: str = ""
    namespaces: list[OntapConsistencyGroupResponseConsistencyGroupNamespace] = Field(
        default_factory=list
    )
    parent_consistency_group: OntapConsistencyGroupResponseConsistencyGroupParentConsistencyGroup = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupParentConsistencyGroup
    )
    provisioning_options: OntapConsistencyGroupResponseConsistencyGroupProvisioningOptions = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupProvisioningOptions
    )
    qos: OntapConsistencyGroupResponseConsistencyGroupQos = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupQos
    )
    restore_to: OntapConsistencyGroupResponseConsistencyGroupRestoreTo = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupRestoreTo
    )
    snapshot_policy: OntapConsistencyGroupResponseConsistencyGroupSnapshotPolicy = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupSnapshotPolicy
    )
    space: OntapConsistencyGroupResponseConsistencyGroupSpace = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupSpace
    )
    svm: OntapConsistencyGroupResponseConsistencyGroupSvm = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupSvm
    )
    tiering: OntapConsistencyGroupResponseConsistencyGroupTiering = Field(
        default_factory=OntapConsistencyGroupResponseConsistencyGroupTiering
    )
    uuid: str = ""
    volumes: list[OntapConsistencyGroupResponseConsistencyGroupVolume] = Field(default_factory=list)


class OntapConsistencyGroupResponseLunCloneSource(OntapModel):
    """OntapConsistencyGroupResponseLunCloneSource sub-model for source."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseLunClone(OntapModel):
    """OntapConsistencyGroupResponseLunClone sub-model for clone."""

    source: OntapConsistencyGroupResponseLunCloneSource = Field(
        default_factory=OntapConsistencyGroupResponseLunCloneSource
    )


class OntapConsistencyGroupResponseLunLunMapIgroupIgroup(OntapModel):
    """OntapConsistencyGroupResponseLunLunMapIgroupIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseLunLunMapIgroupInitiator(OntapModel):
    """OntapConsistencyGroupResponseLunLunMapIgroupInitiator sub-model for initiators."""

    comment: str = ""
    name: str = ""


class OntapConsistencyGroupResponseLunLunMapIgroup(OntapModel):
    """OntapConsistencyGroupResponseLunLunMapIgroup sub-model for igroup."""

    comment: str = ""
    igroups: list[OntapConsistencyGroupResponseLunLunMapIgroupIgroup] = Field(default_factory=list)
    initiators: list[OntapConsistencyGroupResponseLunLunMapIgroupInitiator] = Field(
        default_factory=list
    )
    name: str = ""
    os_type: str = ""
    protocol: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseLunLunMap(OntapModel):
    """OntapConsistencyGroupResponseLunLunMap sub-model for lun_maps."""

    igroup: OntapConsistencyGroupResponseLunLunMapIgroup = Field(
        default_factory=OntapConsistencyGroupResponseLunLunMapIgroup
    )
    logical_unit_number: int = 0


class OntapConsistencyGroupResponseLunProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseLunProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    count: int = 0


class OntapConsistencyGroupResponseLunQosPolicy(OntapModel):
    """OntapConsistencyGroupResponseLunQosPolicy sub-model for policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseLunQos(OntapModel):
    """OntapConsistencyGroupResponseLunQos sub-model for qos."""

    policy: OntapConsistencyGroupResponseLunQosPolicy = Field(
        default_factory=OntapConsistencyGroupResponseLunQosPolicy
    )


class OntapConsistencyGroupResponseLunSpaceGuarantee(OntapModel):
    """OntapConsistencyGroupResponseLunSpaceGuarantee sub-model for guarantee."""

    requested: bool = False
    reserved: bool = False


class OntapConsistencyGroupResponseLunSpace(OntapModel):
    """OntapConsistencyGroupResponseLunSpace sub-model for space."""

    guarantee: OntapConsistencyGroupResponseLunSpaceGuarantee = Field(
        default_factory=OntapConsistencyGroupResponseLunSpaceGuarantee
    )
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseLun(OntapModel):
    """OntapConsistencyGroupResponseLun sub-model for luns."""

    clone: OntapConsistencyGroupResponseLunClone = Field(
        default_factory=OntapConsistencyGroupResponseLunClone
    )
    comment: str = ""
    create_time: str = ""
    enabled: bool = False
    lun_maps: list[OntapConsistencyGroupResponseLunLunMap] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    provisioning_options: OntapConsistencyGroupResponseLunProvisioningOptions = Field(
        default_factory=OntapConsistencyGroupResponseLunProvisioningOptions
    )
    qos: OntapConsistencyGroupResponseLunQos = Field(
        default_factory=OntapConsistencyGroupResponseLunQos
    )
    serial_number: str = ""
    space: OntapConsistencyGroupResponseLunSpace = Field(
        default_factory=OntapConsistencyGroupResponseLunSpace
    )
    uuid: str = ""


class OntapConsistencyGroupResponseMetricIops(OntapModel):
    """OntapConsistencyGroupResponseMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupResponseMetricLatency(OntapModel):
    """OntapConsistencyGroupResponseMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupResponseMetricThroughput(OntapModel):
    """OntapConsistencyGroupResponseMetricThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupResponseMetric(OntapModel):
    """OntapConsistencyGroupResponseMetric sub-model for metric."""

    available_space: int = 0
    duration: str = ""
    iops: OntapConsistencyGroupResponseMetricIops = Field(
        default_factory=OntapConsistencyGroupResponseMetricIops
    )
    latency: OntapConsistencyGroupResponseMetricLatency = Field(
        default_factory=OntapConsistencyGroupResponseMetricLatency
    )
    size: int = 0
    status: str = ""
    throughput: OntapConsistencyGroupResponseMetricThroughput = Field(
        default_factory=OntapConsistencyGroupResponseMetricThroughput
    )
    timestamp: str = ""
    used_space: int = 0


class OntapConsistencyGroupResponseNamespaceProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseNamespaceProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    count: int = 0


class OntapConsistencyGroupResponseNamespaceSpaceGuarantee(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSpaceGuarantee sub-model for guarantee."""

    requested: bool = False
    reserved: bool = False


class OntapConsistencyGroupResponseNamespaceSpace(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSpace sub-model for space."""

    block_size: int = 0
    guarantee: OntapConsistencyGroupResponseNamespaceSpaceGuarantee = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceSpaceGuarantee
    )
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseNamespaceStatus(OntapModel):
    """OntapConsistencyGroupResponseNamespaceStatus sub-model for status."""

    container_state: str = ""
    mapped: bool = False
    read_only: bool = False
    state: str = ""


class OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostDhHmacChap(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostDhHmacChap sub-model for dh_hmac_chap."""

    controller_secret_key: str = ""
    group_size: str = ""
    hash_function: str = ""
    host_secret_key: str = ""
    mode: str = ""


class OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostTls(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostTls sub-model for tls."""

    configured_psk: str = ""
    key_type: str = ""


class OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHost(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHost sub-model for hosts."""

    dh_hmac_chap: OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostDhHmacChap = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostDhHmacChap
    )
    nqn: str = ""
    priority: str = ""
    tls: OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostTls = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHostTls
    )


class OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystem(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystem sub-model for subsystem."""

    comment: str = ""
    hosts: list[OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystemHost] = Field(
        default_factory=list
    )
    name: str = ""
    os_type: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseNamespaceSubsystemMap(OntapModel):
    """OntapConsistencyGroupResponseNamespaceSubsystemMap sub-model for subsystem_map."""

    anagrpid: str = ""
    nsid: str = ""
    subsystem: OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystem = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceSubsystemMapSubsystem
    )


class OntapConsistencyGroupResponseNamespace(OntapModel):
    """OntapConsistencyGroupResponseNamespace sub-model for namespaces."""

    auto_delete: bool = False
    comment: str = ""
    create_time: str = ""
    enabled: bool = False
    name: str = ""
    os_type: str = ""
    provisioning_options: OntapConsistencyGroupResponseNamespaceProvisioningOptions = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceProvisioningOptions
    )
    space: OntapConsistencyGroupResponseNamespaceSpace = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceSpace
    )
    status: OntapConsistencyGroupResponseNamespaceStatus = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceStatus
    )
    subsystem_map: OntapConsistencyGroupResponseNamespaceSubsystemMap = Field(
        default_factory=OntapConsistencyGroupResponseNamespaceSubsystemMap
    )
    uuid: str = ""


class OntapConsistencyGroupResponseParentConsistencyGroup(OntapModel):
    """OntapConsistencyGroupResponseParentConsistencyGroup sub-model for parent_consistency_group."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseProvisioningOptionsStorageService(OntapModel):
    """OntapConsistencyGroupResponseProvisioningOptionsStorageService sub-model for storage_service."""

    name: str = ""


class OntapConsistencyGroupResponseProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    name: str = ""
    storage_service: OntapConsistencyGroupResponseProvisioningOptionsStorageService = Field(
        default_factory=OntapConsistencyGroupResponseProvisioningOptionsStorageService
    )


class OntapConsistencyGroupResponseQosPolicy(OntapModel):
    """OntapConsistencyGroupResponseQosPolicy sub-model for policy."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseQos(OntapModel):
    """OntapConsistencyGroupResponseQos sub-model for qos."""

    policy: OntapConsistencyGroupResponseQosPolicy = Field(
        default_factory=OntapConsistencyGroupResponseQosPolicy
    )


class OntapConsistencyGroupResponseReplicationRelationship(OntapModel):
    """OntapConsistencyGroupResponseReplicationRelationship sub-model for replication_relationships."""

    is_protected_by_svm_dr: bool = False
    is_source: bool = False
    uuid: str = ""


class OntapConsistencyGroupResponseRestoreToSnapshot(OntapModel):
    """OntapConsistencyGroupResponseRestoreToSnapshot sub-model for snapshot."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseRestoreTo(OntapModel):
    """OntapConsistencyGroupResponseRestoreTo sub-model for restore_to."""

    snapshot: OntapConsistencyGroupResponseRestoreToSnapshot = Field(
        default_factory=OntapConsistencyGroupResponseRestoreToSnapshot
    )


class OntapConsistencyGroupResponseSnapshotPolicy(OntapModel):
    """OntapConsistencyGroupResponseSnapshotPolicy sub-model for snapshot_policy."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseSpace(OntapModel):
    """OntapConsistencyGroupResponseSpace sub-model for space."""

    available: int = 0
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseStatisticsIopsRaw(OntapModel):
    """OntapConsistencyGroupResponseStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupResponseStatisticsLatencyRaw(OntapModel):
    """OntapConsistencyGroupResponseStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupResponseStatisticsThroughputRaw(OntapModel):
    """OntapConsistencyGroupResponseStatisticsThroughputRaw sub-model for throughput_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupResponseStatistics(OntapModel):
    """OntapConsistencyGroupResponseStatistics sub-model for statistics."""

    available_space: int = 0
    iops_raw: OntapConsistencyGroupResponseStatisticsIopsRaw = Field(
        default_factory=OntapConsistencyGroupResponseStatisticsIopsRaw
    )
    latency_raw: OntapConsistencyGroupResponseStatisticsLatencyRaw = Field(
        default_factory=OntapConsistencyGroupResponseStatisticsLatencyRaw
    )
    size: int = 0
    status: str = ""
    throughput_raw: OntapConsistencyGroupResponseStatisticsThroughputRaw = Field(
        default_factory=OntapConsistencyGroupResponseStatisticsThroughputRaw
    )
    timestamp: str = ""
    used_space: int = 0


class OntapConsistencyGroupResponseSvm(OntapModel):
    """OntapConsistencyGroupResponseSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseTieringObjectStore(OntapModel):
    """OntapConsistencyGroupResponseTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapConsistencyGroupResponseTiering(OntapModel):
    """OntapConsistencyGroupResponseTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapConsistencyGroupResponseTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapConsistencyGroupResponseVolumeNasCifsShareAcl(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasCifsShareAcl sub-model for acls."""

    permission: str = ""
    type_: str = ""
    user_or_group: str = ""
    win_sid_unix_id: str = ""


class OntapConsistencyGroupResponseVolumeNasCifsShare(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasCifsShare sub-model for shares."""

    access_based_enumeration: bool = False
    acls: list[OntapConsistencyGroupResponseVolumeNasCifsShareAcl] = Field(default_factory=list)
    allow_unencrypted_access: bool = False
    change_notify: bool = False
    comment: str = ""
    continuously_available: bool = False
    dir_umask: int = 0
    encryption: bool = False
    file_umask: int = 0
    home_directory: bool = False
    name: str = ""
    namespace_caching: bool = False
    no_strict_security: bool = False
    offline_files: str = ""
    oplocks: bool = False
    show_snapshot: bool = False
    unix_symlink: str = ""
    vscan_profile: str = ""


class OntapConsistencyGroupResponseVolumeNasCifs(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasCifs sub-model for cifs."""

    shares: list[OntapConsistencyGroupResponseVolumeNasCifsShare] = Field(default_factory=list)


class OntapConsistencyGroupResponseVolumeNasExportPolicyRuleClient(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasExportPolicyRuleClient sub-model for clients."""

    match: str = ""


class OntapConsistencyGroupResponseVolumeNasExportPolicyRule(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasExportPolicyRule sub-model for rules."""

    allow_device_creation: bool = False
    allow_suid: bool = False
    anonymous_user: str = ""
    chown_mode: str = ""
    clients: list[OntapConsistencyGroupResponseVolumeNasExportPolicyRuleClient] = Field(
        default_factory=list
    )
    index: int = 0
    ntfs_unix_security: str = ""
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)


class OntapConsistencyGroupResponseVolumeNasExportPolicy(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasExportPolicy sub-model for export_policy."""

    id: int = 0
    name: str = ""
    rules: list[OntapConsistencyGroupResponseVolumeNasExportPolicyRule] = Field(
        default_factory=list
    )


class OntapConsistencyGroupResponseVolumeNasJunctionParent(OntapModel):
    """OntapConsistencyGroupResponseVolumeNasJunctionParent sub-model for junction_parent."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseVolumeNas(OntapModel):
    """OntapConsistencyGroupResponseVolumeNas sub-model for nas."""

    cifs: OntapConsistencyGroupResponseVolumeNasCifs = Field(
        default_factory=OntapConsistencyGroupResponseVolumeNasCifs
    )
    export_policy: OntapConsistencyGroupResponseVolumeNasExportPolicy = Field(
        default_factory=OntapConsistencyGroupResponseVolumeNasExportPolicy
    )
    gid: int = 0
    junction_parent: OntapConsistencyGroupResponseVolumeNasJunctionParent = Field(
        default_factory=OntapConsistencyGroupResponseVolumeNasJunctionParent
    )
    path: str = ""
    security_style: str = ""
    uid: int = 0
    unix_permissions: int = 0


class OntapConsistencyGroupResponseVolumeProvisioningOptionsStorageService(OntapModel):
    """OntapConsistencyGroupResponseVolumeProvisioningOptionsStorageService sub-model for storage_service."""

    name: str = ""


class OntapConsistencyGroupResponseVolumeProvisioningOptions(OntapModel):
    """OntapConsistencyGroupResponseVolumeProvisioningOptions sub-model for provisioning_options."""

    action: str = ""
    count: int = 0
    storage_service: OntapConsistencyGroupResponseVolumeProvisioningOptionsStorageService = Field(
        default_factory=OntapConsistencyGroupResponseVolumeProvisioningOptionsStorageService
    )


class OntapConsistencyGroupResponseVolumeQosPolicy(OntapModel):
    """OntapConsistencyGroupResponseVolumeQosPolicy sub-model for policy."""

    name: str = ""
    uuid: str = ""


class OntapConsistencyGroupResponseVolumeQos(OntapModel):
    """OntapConsistencyGroupResponseVolumeQos sub-model for qos."""

    policy: OntapConsistencyGroupResponseVolumeQosPolicy = Field(
        default_factory=OntapConsistencyGroupResponseVolumeQosPolicy
    )


class OntapConsistencyGroupResponseVolumeSpace(OntapModel):
    """OntapConsistencyGroupResponseVolumeSpace sub-model for space."""

    available: int = 0
    size: int = 0
    used: int = 0


class OntapConsistencyGroupResponseVolumeTieringObjectStore(OntapModel):
    """OntapConsistencyGroupResponseVolumeTieringObjectStore sub-model for object_stores."""

    name: str = ""


class OntapConsistencyGroupResponseVolumeTiering(OntapModel):
    """OntapConsistencyGroupResponseVolumeTiering sub-model for tiering."""

    control: str = ""
    object_stores: list[OntapConsistencyGroupResponseVolumeTieringObjectStore] = Field(
        default_factory=list
    )
    policy: str = ""


class OntapConsistencyGroupResponseVolume(OntapModel):
    """OntapConsistencyGroupResponseVolume sub-model for volumes."""

    comment: str = ""
    name: str = ""
    nas: OntapConsistencyGroupResponseVolumeNas = Field(
        default_factory=OntapConsistencyGroupResponseVolumeNas
    )
    provisioning_options: OntapConsistencyGroupResponseVolumeProvisioningOptions = Field(
        default_factory=OntapConsistencyGroupResponseVolumeProvisioningOptions
    )
    qos: OntapConsistencyGroupResponseVolumeQos = Field(
        default_factory=OntapConsistencyGroupResponseVolumeQos
    )
    space: OntapConsistencyGroupResponseVolumeSpace = Field(
        default_factory=OntapConsistencyGroupResponseVolumeSpace
    )
    tiering: OntapConsistencyGroupResponseVolumeTiering = Field(
        default_factory=OntapConsistencyGroupResponseVolumeTiering
    )
    uuid: str = ""


class OntapConsistencyGroupResponse(OntapModel):
    """OntapConsistencyGroupResponse information."""

    application: OntapConsistencyGroupResponseApplication = Field(
        default_factory=OntapConsistencyGroupResponseApplication
    )
    clone: OntapConsistencyGroupResponseClone = Field(
        default_factory=OntapConsistencyGroupResponseClone
    )
    consistency_groups: list[OntapConsistencyGroupResponseConsistencyGroup] = Field(
        default_factory=list
    )
    luns: list[OntapConsistencyGroupResponseLun] = Field(default_factory=list)
    metric: OntapConsistencyGroupResponseMetric = Field(
        default_factory=OntapConsistencyGroupResponseMetric
    )
    name: str = ""
    namespaces: list[OntapConsistencyGroupResponseNamespace] = Field(default_factory=list)
    parent_consistency_group: OntapConsistencyGroupResponseParentConsistencyGroup = Field(
        default_factory=OntapConsistencyGroupResponseParentConsistencyGroup
    )
    provisioning_options: OntapConsistencyGroupResponseProvisioningOptions = Field(
        default_factory=OntapConsistencyGroupResponseProvisioningOptions
    )
    qos: OntapConsistencyGroupResponseQos = Field(default_factory=OntapConsistencyGroupResponseQos)
    replicated: bool = False
    replication_relationships: list[OntapConsistencyGroupResponseReplicationRelationship] = Field(
        default_factory=list
    )
    replication_source: bool = False
    restore_to: OntapConsistencyGroupResponseRestoreTo = Field(
        default_factory=OntapConsistencyGroupResponseRestoreTo
    )
    snapshot_policy: OntapConsistencyGroupResponseSnapshotPolicy = Field(
        default_factory=OntapConsistencyGroupResponseSnapshotPolicy
    )
    space: OntapConsistencyGroupResponseSpace = Field(
        default_factory=OntapConsistencyGroupResponseSpace
    )
    statistics: OntapConsistencyGroupResponseStatistics = Field(
        default_factory=OntapConsistencyGroupResponseStatistics
    )
    svm: OntapConsistencyGroupResponseSvm = Field(default_factory=OntapConsistencyGroupResponseSvm)
    tiering: OntapConsistencyGroupResponseTiering = Field(
        default_factory=OntapConsistencyGroupResponseTiering
    )
    uuid: str = ""
    volumes: list[OntapConsistencyGroupResponseVolume] = Field(default_factory=list)
