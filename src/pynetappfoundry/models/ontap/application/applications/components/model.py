"""OntapApplicationComponent information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationComponentApplication(OntapModel):
    """OntapApplicationComponentApplication sub-model for application."""

    name: str = ""
    uuid: str = ""


class OntapApplicationComponentBackingStorageLun(OntapModel):
    """OntapApplicationComponentBackingStorageLun sub-model for luns."""

    creation_timestamp: str = ""
    path: str = ""
    size: int = 0
    uuid: str = ""


class OntapApplicationComponentBackingStorageNamespace(OntapModel):
    """OntapApplicationComponentBackingStorageNamespace sub-model for namespaces."""

    creation_timestamp: str = ""
    name: str = ""
    size: int = 0
    uuid: str = ""


class OntapApplicationComponentBackingStorageVolume(OntapModel):
    """OntapApplicationComponentBackingStorageVolume sub-model for volumes."""

    creation_timestamp: str = ""
    name: str = ""
    size: int = 0
    uuid: str = ""


class OntapApplicationComponentBackingStorage(OntapModel):
    """OntapApplicationComponentBackingStorage sub-model for backing_storage."""

    luns: list[OntapApplicationComponentBackingStorageLun] = Field(default_factory=list)
    namespaces: list[OntapApplicationComponentBackingStorageNamespace] = Field(default_factory=list)
    volumes: list[OntapApplicationComponentBackingStorageVolume] = Field(default_factory=list)


class OntapApplicationComponentCifsAccessBackingStorage(OntapModel):
    """OntapApplicationComponentCifsAccessBackingStorage sub-model for backing_storage."""

    type_: str = ""
    uuid: str = ""


class OntapApplicationComponentCifsAccessPermission(OntapModel):
    """OntapApplicationComponentCifsAccessPermission sub-model for permissions."""

    access: str = ""
    user_or_group: str = ""


class OntapApplicationComponentCifsAccessServer(OntapModel):
    """OntapApplicationComponentCifsAccessServer sub-model for server."""

    name: str = ""


class OntapApplicationComponentCifsAccessShare(OntapModel):
    """OntapApplicationComponentCifsAccessShare sub-model for share."""

    name: str = ""


class OntapApplicationComponentCifsAccess(OntapModel):
    """OntapApplicationComponentCifsAccess sub-model for cifs_access."""

    backing_storage: OntapApplicationComponentCifsAccessBackingStorage = Field(
        default_factory=OntapApplicationComponentCifsAccessBackingStorage
    )
    ips: list[str] = Field(default_factory=list)
    path: str = ""
    permissions: list[OntapApplicationComponentCifsAccessPermission] = Field(default_factory=list)
    server: OntapApplicationComponentCifsAccessServer = Field(
        default_factory=OntapApplicationComponentCifsAccessServer
    )
    share: OntapApplicationComponentCifsAccessShare = Field(
        default_factory=OntapApplicationComponentCifsAccessShare
    )


class OntapApplicationComponentNfsAccessBackingStorage(OntapModel):
    """OntapApplicationComponentNfsAccessBackingStorage sub-model for backing_storage."""

    type_: str = ""
    uuid: str = ""


class OntapApplicationComponentNfsAccessExportPolicy(OntapModel):
    """OntapApplicationComponentNfsAccessExportPolicy sub-model for export_policy."""

    name: str = ""


class OntapApplicationComponentNfsAccessPermission(OntapModel):
    """OntapApplicationComponentNfsAccessPermission sub-model for permissions."""

    access: str = ""
    host: str = ""


class OntapApplicationComponentNfsAccess(OntapModel):
    """OntapApplicationComponentNfsAccess sub-model for nfs_access."""

    backing_storage: OntapApplicationComponentNfsAccessBackingStorage = Field(
        default_factory=OntapApplicationComponentNfsAccessBackingStorage
    )
    export_policy: OntapApplicationComponentNfsAccessExportPolicy = Field(
        default_factory=OntapApplicationComponentNfsAccessExportPolicy
    )
    ips: list[str] = Field(default_factory=list)
    path: str = ""
    permissions: list[OntapApplicationComponentNfsAccessPermission] = Field(default_factory=list)


class OntapApplicationComponentNvmeAccessBackingStorage(OntapModel):
    """OntapApplicationComponentNvmeAccessBackingStorage sub-model for backing_storage."""

    type_: str = ""
    uuid: str = ""


class OntapApplicationComponentNvmeAccessSubsystemMapSubsystemHost(OntapModel):
    """OntapApplicationComponentNvmeAccessSubsystemMapSubsystemHost sub-model for hosts."""

    nqn: str = ""


class OntapApplicationComponentNvmeAccessSubsystemMapSubsystem(OntapModel):
    """OntapApplicationComponentNvmeAccessSubsystemMapSubsystem sub-model for subsystem."""

    hosts: list[OntapApplicationComponentNvmeAccessSubsystemMapSubsystemHost] = Field(
        default_factory=list
    )
    name: str = ""
    uuid: str = ""


class OntapApplicationComponentNvmeAccessSubsystemMap(OntapModel):
    """OntapApplicationComponentNvmeAccessSubsystemMap sub-model for subsystem_map."""

    anagrpid: str = ""
    nsid: str = ""
    subsystem: OntapApplicationComponentNvmeAccessSubsystemMapSubsystem = Field(
        default_factory=OntapApplicationComponentNvmeAccessSubsystemMapSubsystem
    )


class OntapApplicationComponentNvmeAccess(OntapModel):
    """OntapApplicationComponentNvmeAccess sub-model for nvme_access."""

    backing_storage: OntapApplicationComponentNvmeAccessBackingStorage = Field(
        default_factory=OntapApplicationComponentNvmeAccessBackingStorage
    )
    is_clone: bool = False
    subsystem_map: OntapApplicationComponentNvmeAccessSubsystemMap = Field(
        default_factory=OntapApplicationComponentNvmeAccessSubsystemMap
    )


class OntapApplicationComponentProtectionGroupRpoLocal(OntapModel):
    """OntapApplicationComponentProtectionGroupRpoLocal sub-model for local."""

    description: str = ""
    name: str = ""


class OntapApplicationComponentProtectionGroupRpoRemote(OntapModel):
    """OntapApplicationComponentProtectionGroupRpoRemote sub-model for remote."""

    description: str = ""
    name: str = ""


class OntapApplicationComponentProtectionGroupRpo(OntapModel):
    """OntapApplicationComponentProtectionGroupRpo sub-model for rpo."""

    local: OntapApplicationComponentProtectionGroupRpoLocal = Field(
        default_factory=OntapApplicationComponentProtectionGroupRpoLocal
    )
    remote: OntapApplicationComponentProtectionGroupRpoRemote = Field(
        default_factory=OntapApplicationComponentProtectionGroupRpoRemote
    )


class OntapApplicationComponentProtectionGroup(OntapModel):
    """OntapApplicationComponentProtectionGroup sub-model for protection_groups."""

    name: str = ""
    rpo: OntapApplicationComponentProtectionGroupRpo = Field(
        default_factory=OntapApplicationComponentProtectionGroupRpo
    )
    uuid: str = ""


class OntapApplicationComponentSanAccessBackingStorage(OntapModel):
    """OntapApplicationComponentSanAccessBackingStorage sub-model for backing_storage."""

    type_: str = ""
    uuid: str = ""


class OntapApplicationComponentSanAccessLunMappingIgroup(OntapModel):
    """OntapApplicationComponentSanAccessLunMappingIgroup sub-model for igroup."""

    initiators: list[str] = Field(default_factory=list)
    name: str = ""
    uuid: str = ""


class OntapApplicationComponentSanAccessLunMappingIscsiInterfaceIp(OntapModel):
    """OntapApplicationComponentSanAccessLunMappingIscsiInterfaceIp sub-model for ip."""

    address: str = ""


class OntapApplicationComponentSanAccessLunMappingIscsiInterface(OntapModel):
    """OntapApplicationComponentSanAccessLunMappingIscsiInterface sub-model for interface."""

    ip: OntapApplicationComponentSanAccessLunMappingIscsiInterfaceIp = Field(
        default_factory=OntapApplicationComponentSanAccessLunMappingIscsiInterfaceIp
    )
    name: str = ""
    uuid: str = ""


class OntapApplicationComponentSanAccessLunMappingIscsi(OntapModel):
    """OntapApplicationComponentSanAccessLunMappingIscsi sub-model for iscsi."""

    interface: OntapApplicationComponentSanAccessLunMappingIscsiInterface = Field(
        default_factory=OntapApplicationComponentSanAccessLunMappingIscsiInterface
    )
    port: int = 0


class OntapApplicationComponentSanAccessLunMapping(OntapModel):
    """OntapApplicationComponentSanAccessLunMapping sub-model for lun_mappings."""

    fcp: list[dict[str, Any]] = Field(default_factory=list)
    igroup: OntapApplicationComponentSanAccessLunMappingIgroup = Field(
        default_factory=OntapApplicationComponentSanAccessLunMappingIgroup
    )
    iscsi: list[OntapApplicationComponentSanAccessLunMappingIscsi] = Field(default_factory=list)
    lun_id: int = 0


class OntapApplicationComponentSanAccess(OntapModel):
    """OntapApplicationComponentSanAccess sub-model for san_access."""

    backing_storage: OntapApplicationComponentSanAccessBackingStorage = Field(
        default_factory=OntapApplicationComponentSanAccessBackingStorage
    )
    is_clone: bool = False
    lun_mappings: list[OntapApplicationComponentSanAccessLunMapping] = Field(default_factory=list)
    serial_number: str = ""


class OntapApplicationComponentStorageService(OntapModel):
    """OntapApplicationComponentStorageService sub-model for storage_service."""

    name: str = ""
    uuid: str = ""


class OntapApplicationComponentSvm(OntapModel):
    """OntapApplicationComponentSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapApplicationComponent(OntapModel):
    """OntapApplicationComponent information."""

    application: OntapApplicationComponentApplication = Field(
        default_factory=OntapApplicationComponentApplication
    )
    backing_storage: OntapApplicationComponentBackingStorage = Field(
        default_factory=OntapApplicationComponentBackingStorage
    )
    cifs_access: list[OntapApplicationComponentCifsAccess] = Field(default_factory=list)
    file_system: str = ""
    host_management_url: str = ""
    host_name: str = ""
    name: str = ""
    nfs_access: list[OntapApplicationComponentNfsAccess] = Field(default_factory=list)
    nvme_access: list[OntapApplicationComponentNvmeAccess] = Field(default_factory=list)
    protection_groups: list[OntapApplicationComponentProtectionGroup] = Field(default_factory=list)
    san_access: list[OntapApplicationComponentSanAccess] = Field(default_factory=list)
    storage_service: OntapApplicationComponentStorageService = Field(
        default_factory=OntapApplicationComponentStorageService
    )
    svm: OntapApplicationComponentSvm = Field(default_factory=OntapApplicationComponentSvm)
    uuid: str = ""
