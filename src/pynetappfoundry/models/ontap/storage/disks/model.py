"""OntapDisk information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDiskAggregate(OntapModel):
    """OntapDiskAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapDiskDrNode(OntapModel):
    """OntapDiskDrNode sub-model for dr_node."""

    name: str = ""
    uuid: str = ""


class OntapDiskDrawer(OntapModel):
    """OntapDiskDrawer sub-model for drawer."""

    id: int = 0
    slot: int = 0


class OntapDiskErrorReasonArgument(OntapModel):
    """OntapDiskErrorReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapDiskErrorReason(OntapModel):
    """OntapDiskErrorReason sub-model for reason."""

    arguments: list[OntapDiskErrorReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapDiskError(OntapModel):
    """OntapDiskError sub-model for error."""

    reason: OntapDiskErrorReason = Field(default_factory=OntapDiskErrorReason)
    type_: str = ""


class OntapDiskHomeNode(OntapModel):
    """OntapDiskHomeNode sub-model for home_node."""

    name: str = ""
    uuid: str = ""


class OntapDiskKeyId(OntapModel):
    """OntapDiskKeyId sub-model for key_id."""

    data: str = ""
    fips: str = ""


class OntapDiskNode(OntapModel):
    """OntapDiskNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapDiskOutageReasonArgument(OntapModel):
    """OntapDiskOutageReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapDiskOutageReason(OntapModel):
    """OntapDiskOutageReason sub-model for reason."""

    arguments: list[OntapDiskOutageReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapDiskOutage(OntapModel):
    """OntapDiskOutage sub-model for outage."""

    persistently_failed: bool = False
    reason: OntapDiskOutageReason = Field(default_factory=OntapDiskOutageReason)


class OntapDiskPath(OntapModel):
    """OntapDiskPath sub-model for paths."""

    disk_path_name: str = ""
    initiator: str = ""
    name: str = ""
    uuid: str = ""
    port_name: str = ""
    port_type: str = ""
    vmdisk_hypervisor_file_name: str = ""
    wwnn: str = ""
    wwpn: str = ""


class OntapDiskShelf(OntapModel):
    """OntapDiskShelf sub-model for shelf."""

    uid: str = ""


class OntapDiskStats(OntapModel):
    """OntapDiskStats sub-model for stats."""

    average_latency: int = 0
    iops_total: int = 0
    path_error_count: int = 0
    power_on_hours: int = 0
    throughput: int = 0


class OntapDiskStoragePool(OntapModel):
    """OntapDiskStoragePool sub-model for storage_pool."""

    name: str = ""
    uuid: str = ""


class OntapDiskVirtual(OntapModel):
    """OntapDiskVirtual sub-model for virtual."""

    container: str = ""
    object: str = ""
    storage_account: str = ""
    target_address: str = ""


class OntapDisk(OntapModel):
    """OntapDisk information."""

    aggregates: list[OntapDiskAggregate] = Field(default_factory=list)
    bay: int = 0
    bytes_per_sector: int = 0
    class_: str = ""
    compliance_standard: str = ""
    container_type: str = ""
    control_standard: str = ""
    dr_node: OntapDiskDrNode = Field(default_factory=OntapDiskDrNode)
    drawer: OntapDiskDrawer = Field(default_factory=OntapDiskDrawer)
    effective_type: str = ""
    encryption_operation: str = ""
    error: list[OntapDiskError] = Field(default_factory=list)
    fips_certified: bool = False
    firmware_version: str = ""
    home_node: OntapDiskHomeNode = Field(default_factory=OntapDiskHomeNode)
    key_id: OntapDiskKeyId = Field(default_factory=OntapDiskKeyId)
    local: bool = False
    location: str = ""
    model_: str = ""
    name: str = ""
    node: OntapDiskNode = Field(default_factory=OntapDiskNode)
    outage: OntapDiskOutage = Field(default_factory=OntapDiskOutage)
    overall_security: str = ""
    paths: list[OntapDiskPath] = Field(default_factory=list)
    physical_size: int = 0
    pool: str = ""
    protection_mode: str = ""
    rated_life_used_percent: int = 0
    right_size_sector_count: int = 0
    rpm: int = 0
    sanitize_spare: bool = False
    sector_count: int = 0
    self_encrypting: bool = False
    serial_number: str = ""
    shelf: OntapDiskShelf = Field(default_factory=OntapDiskShelf)
    state: str = ""
    stats: OntapDiskStats = Field(default_factory=OntapDiskStats)
    storage_pool: OntapDiskStoragePool = Field(default_factory=OntapDiskStoragePool)
    type_: str = ""
    uid: str = ""
    usable_size: int = 0
    vendor: str = ""
    virtual: OntapDiskVirtual = Field(default_factory=OntapDiskVirtual)
