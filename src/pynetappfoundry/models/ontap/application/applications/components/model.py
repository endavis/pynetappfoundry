"""OntapApplicationComponent information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationComponentLun(OntapModel):
    """OntapApplicationComponentLun sub-model for luns."""

    backing_storage_luns_creation_timestamp: str = ""
    backing_storage_luns_path: str = ""
    backing_storage_luns_size: int = 0
    backing_storage_luns_uuid: str = ""


class OntapApplicationComponentNamespace(OntapModel):
    """OntapApplicationComponentNamespace sub-model for namespaces."""

    backing_storage_namespaces_creation_timestamp: str = ""
    backing_storage_namespaces_name: str = ""
    backing_storage_namespaces_size: int = 0
    backing_storage_namespaces_uuid: str = ""


class OntapApplicationComponentVolume(OntapModel):
    """OntapApplicationComponentVolume sub-model for volumes."""

    backing_storage_volumes_creation_timestamp: str = ""
    backing_storage_volumes_name: str = ""
    backing_storage_volumes_size: int = 0
    backing_storage_volumes_uuid: str = ""


class OntapApplicationComponentCifsAccess(OntapModel):
    """OntapApplicationComponentCifsAccess sub-model for cifs_access."""

    cifs_access_backing_storage_type: str = ""
    cifs_access_backing_storage_uuid: str = ""
    cifs_access_ips: list[str] = Field(default_factory=list)
    cifs_access_path: str = ""
    cifs_access_permissions: list[dict[str, Any]] = Field(default_factory=list)
    cifs_access_server_name: str = ""
    cifs_access_share_name: str = ""


class OntapApplicationComponentNfsAccess(OntapModel):
    """OntapApplicationComponentNfsAccess sub-model for nfs_access."""

    nfs_access_backing_storage_type: str = ""
    nfs_access_backing_storage_uuid: str = ""
    nfs_access_export_policy_name: str = ""
    nfs_access_ips: list[str] = Field(default_factory=list)
    nfs_access_path: str = ""
    nfs_access_permissions: list[dict[str, Any]] = Field(default_factory=list)


class OntapApplicationComponentNvmeAccess(OntapModel):
    """OntapApplicationComponentNvmeAccess sub-model for nvme_access."""

    nvme_access_backing_storage_type: str = ""
    nvme_access_backing_storage_uuid: str = ""
    nvme_access_is_clone: bool = False
    nvme_access_subsystem_map_anagrpid: str = ""
    nvme_access_subsystem_map_nsid: str = ""
    nvme_access_subsystem_map_subsystem_hosts: list[dict[str, Any]] = Field(default_factory=list)
    nvme_access_subsystem_map_subsystem_name: str = ""
    nvme_access_subsystem_map_subsystem_uuid: str = ""


class OntapApplicationComponentProtectionGroup(OntapModel):
    """OntapApplicationComponentProtectionGroup sub-model for protection_groups."""

    protection_groups_name: str = ""
    protection_groups_rpo_local_description: str = ""
    protection_groups_rpo_local_name: str = ""
    protection_groups_rpo_remote_description: str = ""
    protection_groups_rpo_remote_name: str = ""
    protection_groups_uuid: str = ""


class OntapApplicationComponentSanAccess(OntapModel):
    """OntapApplicationComponentSanAccess sub-model for san_access."""

    san_access_backing_storage_type: str = ""
    san_access_backing_storage_uuid: str = ""
    san_access_is_clone: bool = False
    san_access_lun_mappings: list[dict[str, Any]] = Field(default_factory=list)
    san_access_serial_number: str = ""


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
