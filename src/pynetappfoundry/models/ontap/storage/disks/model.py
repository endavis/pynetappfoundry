"""OntapDisk information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDiskAggregate(OntapModel):
    """OntapDiskAggregate sub-model for aggregates."""

    aggregates_name: str = ""
    aggregates_uuid: str = ""


class OntapDiskError(OntapModel):
    """OntapDiskError sub-model for error."""

    error_reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    error_reason_code: str = ""
    error_reason_message: str = ""
    error_type: str = ""


class OntapDiskArgument(OntapModel):
    """OntapDiskArgument sub-model for arguments."""

    outage_reason_arguments_code: str = ""
    outage_reason_arguments_message: str = ""


class OntapDiskPath(OntapModel):
    """OntapDiskPath sub-model for paths."""

    paths_disk_path_name: str = ""
    paths_initiator: str = ""
    paths_node_name: str = ""
    paths_node_uuid: str = ""
    paths_port_name: str = ""
    paths_port_type: str = ""
    paths_vmdisk_hypervisor_file_name: str = ""
    paths_wwnn: str = ""
    paths_wwpn: str = ""


class OntapDisk(OntapModel):
    """OntapDisk information."""

    aggregates: list[OntapDiskAggregate] = Field(default_factory=list)
    bay: int = 0
    bytes_per_sector: int = 0
    class_: str = ""
    compliance_standard: str = ""
    container_type: str = ""
    control_standard: str = ""
    dr_node_name: str = ""
    dr_node_uuid: str = ""
    drawer_id: int = 0
    drawer_slot: int = 0
    effective_type: str = ""
    encryption_operation: str = ""
    error: list[OntapDiskError] = Field(default_factory=list)
    fips_certified: bool = False
    firmware_version: str = ""
    home_node_name: str = ""
    home_node_uuid: str = ""
    key_id_data: str = ""
    key_id_fips: str = ""
    local: bool = False
    location: str = ""
    model_: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    outage_persistently_failed: bool = False
    outage_reason_arguments: list[OntapDiskArgument] = Field(default_factory=list)
    outage_reason_code: str = ""
    outage_reason_message: str = ""
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
    shelf_uid: str = ""
    state: str = ""
    stats_average_latency: int = 0
    stats_iops_total: int = 0
    stats_path_error_count: int = 0
    stats_power_on_hours: int = 0
    stats_throughput: int = 0
    storage_pool_name: str = ""
    storage_pool_uuid: str = ""
    type_: str = ""
    uid: str = ""
    usable_size: int = 0
    vendor: str = ""
    virtual_container: str = ""
    virtual_object: str = ""
    virtual_storage_account: str = ""
    virtual_target_address: str = ""
