"""Protocol service and configuration models (/protocols API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ExportRuleInfo(BaseModel):
    """Export rule within an export policy."""

    model_config = ConfigDict(extra="allow")

    index: int = 0
    clients: list[str] = Field(default_factory=list)
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)
    anonymous_user: str = ""


class ExportPolicyInfo(BaseModel):
    """NFS export policy information."""

    model_config = ConfigDict(extra="allow")

    id: int = 0
    name: str = ""
    svm: str = ""
    rules: list[ExportRuleInfo] = Field(default_factory=list)


class QtreeInfo(BaseModel):
    """Qtree information."""

    model_config = ConfigDict(extra="allow")

    id: int = 0
    name: str = ""
    svm: str = ""
    volume: str = ""
    path: str = ""
    security_style: str = ""  # unix, ntfs, mixed
    unix_permissions: str = ""
    export_policy: str = ""


class NFSServiceInfo(BaseModel):
    """NFS service configuration per SVM."""

    model_config = ConfigDict(extra="allow")

    svm: str = ""
    enabled: bool = False
    protocol_v3_enabled: bool = False
    protocol_v4_enabled: bool = False
    protocol_v41_enabled: bool = False
    showmount_enabled: bool = False
    vstorage_enabled: bool = False


class CIFSServiceInfo(BaseModel):
    """CIFS/SMB service configuration per SVM."""

    model_config = ConfigDict(extra="allow")

    svm: str = ""
    name: str = ""  # CIFS server name
    enabled: bool = False
    ad_domain: str = ""
    comment: str = ""
    default_unix_user: str = ""
    netbios_aliases: list[str] = Field(default_factory=list)


class CIFSShareInfo(BaseModel):
    """CIFS/SMB share information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    path: str = ""
    svm: str = ""
    comment: str = ""
    home_directory: bool = False
    oplocks: bool = True
    access_based_enumeration: bool = False
    change_notify: bool = True
    encryption: bool = False
    unix_symlink: str = ""  # local, widelink, disable


class S3BucketInfo(BaseModel):
    """S3 bucket information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    type: str = ""  # s3, nas-s3
    size: int = 0  # bytes
    versioning_state: str = ""  # enabled, disabled, suspended
    comment: str = ""
    nas_path: str = ""


class LunInfo(BaseModel):
    """LUN (Logical Unit Number) information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    volume: str = ""
    size: int = 0  # bytes
    os_type: str = ""  # linux, windows, vmware, etc.
    serial_number: str = ""
    enabled: bool = True
    comment: str = ""
    qos_policy: str = ""
    create_time: str = ""


class IgroupInfo(BaseModel):
    """Initiator group information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    protocol: str = ""  # fcp, iscsi, mixed
    os_type: str = ""  # linux, windows, vmware, etc.
    initiators: list[str] = Field(default_factory=list)
    comment: str = ""
