"""OntapStoragePool information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStoragePoolDisk(OntapModel):
    """OntapStoragePoolDisk sub-model for disks."""

    disk_name: str = ""
    total_size: int = 0
    usable_size: int = 0


class OntapStoragePoolSpareAllocationUnit(OntapModel):
    """OntapStoragePoolSpareAllocationUnit sub-model for spare_allocation_units."""

    available_size: int = 0
    count: int = 0
    node_name: str = ""
    node_uuid: str = ""
    size: int = 0
    syncmirror_pool: str = ""


class OntapStoragePoolUsedAllocationUnit(OntapModel):
    """OntapStoragePoolUsedAllocationUnit sub-model for used_allocation_units."""

    aggregate_name: str = ""
    aggregate_uuid: str = ""
    count: int = 0
    current_usage: int = 0
    node_name: str = ""
    node_uuid: str = ""


class OntapStoragePoolArgument(OntapModel):
    """OntapStoragePoolArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapStoragePoolNode(OntapModel):
    """OntapStoragePoolNode sub-model for nodes."""

    name: str = ""
    uuid: str = ""


class OntapStoragePool(OntapModel):
    """OntapStoragePool information."""

    capacity_disk_count: int = 0
    capacity_disks: list[OntapStoragePoolDisk] = Field(default_factory=list)
    capacity_remaining: int = 0
    capacity_spare_allocation_units: list[OntapStoragePoolSpareAllocationUnit] = Field(
        default_factory=list
    )
    capacity_total: int = 0
    capacity_used_allocation_units: list[OntapStoragePoolUsedAllocationUnit] = Field(
        default_factory=list
    )
    health_is_healthy: bool = False
    health_state: str = ""
    health_unhealthy_reason_arguments: list[OntapStoragePoolArgument] = Field(default_factory=list)
    health_unhealthy_reason_code: str = ""
    health_unhealthy_reason_message: str = ""
    name: str = ""
    nodes: list[OntapStoragePoolNode] = Field(default_factory=list)
    storage_type: str = ""
    uuid: str = ""
