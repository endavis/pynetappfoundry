"""OntapApplicationComponent information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationComponentLun(OntapModel):
    """OntapApplicationComponentLun sub-model for luns."""

    creation_timestamp: str = ""
    path: str = ""
    size: int = 0
    uuid: str = ""


class OntapApplicationComponentNamespace(OntapModel):
    """OntapApplicationComponentNamespace sub-model for namespaces."""

    creation_timestamp: str = ""
    name: str = ""
    size: int = 0
    uuid: str = ""


class OntapApplicationComponentVolume(OntapModel):
    """OntapApplicationComponentVolume sub-model for volumes."""

    creation_timestamp: str = ""
    name: str = ""
    size: int = 0
    uuid: str = ""


class OntapApplicationComponentCifsAccess(OntapModel):
    """OntapApplicationComponentCifsAccess sub-model for cifs_access."""

    backing_storage_type: str = ""
    backing_storage_uuid: str = ""
    ips: list[str] = Field(default_factory=list)
    path: str = ""
    permissions: list[dict[str, Any]] = Field(default_factory=list)
    server_name: str = ""
    share_name: str = ""


class OntapApplicationComponentNfsAccess(OntapModel):
    """OntapApplicationComponentNfsAccess sub-model for nfs_access."""

    backing_storage_type: str = ""
    backing_storage_uuid: str = ""
    export_policy_name: str = ""
    ips: list[str] = Field(default_factory=list)
    path: str = ""
    permissions: list[dict[str, Any]] = Field(default_factory=list)


class OntapApplicationComponentNvmeAccess(OntapModel):
    """OntapApplicationComponentNvmeAccess sub-model for nvme_access."""

    backing_storage_type: str = ""
    backing_storage_uuid: str = ""
    is_clone: bool = False
    subsystem_map_anagrpid: str = ""
    subsystem_map_nsid: str = ""
    subsystem_map_subsystem_hosts: list[dict[str, Any]] = Field(default_factory=list)
    subsystem_map_subsystem_name: str = ""
    subsystem_map_subsystem_uuid: str = ""


class OntapApplicationComponentProtectionGroup(OntapModel):
    """OntapApplicationComponentProtectionGroup sub-model for protection_groups."""

    name: str = ""
    rpo_local_description: str = ""
    rpo_local_name: str = ""
    rpo_remote_description: str = ""
    rpo_remote_name: str = ""
    uuid: str = ""


class OntapApplicationComponentSanAccess(OntapModel):
    """OntapApplicationComponentSanAccess sub-model for san_access."""

    backing_storage_type: str = ""
    backing_storage_uuid: str = ""
    is_clone: bool = False
    lun_mappings: list[dict[str, Any]] = Field(default_factory=list)
    serial_number: str = ""


class OntapApplicationComponent(OntapModel):
    """OntapApplicationComponent information."""

    application_name: str = ""
    application_uuid: str = ""
    backing_storage_luns: list[OntapApplicationComponentLun] = Field(default_factory=list)
    backing_storage_namespaces: list[OntapApplicationComponentNamespace] = Field(
        default_factory=list
    )
    backing_storage_volumes: list[OntapApplicationComponentVolume] = Field(default_factory=list)
    cifs_access: list[OntapApplicationComponentCifsAccess] = Field(default_factory=list)
    file_system: str = ""
    host_management_url: str = ""
    host_name: str = ""
    name: str = ""
    nfs_access: list[OntapApplicationComponentNfsAccess] = Field(default_factory=list)
    nvme_access: list[OntapApplicationComponentNvmeAccess] = Field(default_factory=list)
    protection_groups: list[OntapApplicationComponentProtectionGroup] = Field(default_factory=list)
    san_access: list[OntapApplicationComponentSanAccess] = Field(default_factory=list)
    storage_service_name: str = ""
    storage_service_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
