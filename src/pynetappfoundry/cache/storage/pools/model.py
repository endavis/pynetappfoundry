"""OntapStoragePool information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapStoragePoolDisk(CacheModel):
    """OntapStoragePoolDisk sub-model for disks."""

    capacity_disks_disk_name: str = ""
    capacity_disks_total_size: int = 0
    capacity_disks_usable_size: int = 0


class OntapStoragePoolSpareAllocationUnit(CacheModel):
    """OntapStoragePoolSpareAllocationUnit sub-model for spare_allocation_units."""

    capacity_spare_allocation_units_available_size: int = 0
    capacity_spare_allocation_units_count: int = 0
    capacity_spare_allocation_units_node_name: str = ""
    capacity_spare_allocation_units_node_uuid: str = ""
    capacity_spare_allocation_units_size: int = 0
    capacity_spare_allocation_units_syncmirror_pool: str = ""


class OntapStoragePoolUsedAllocationUnit(CacheModel):
    """OntapStoragePoolUsedAllocationUnit sub-model for used_allocation_units."""

    capacity_used_allocation_units_aggregate_name: str = ""
    capacity_used_allocation_units_aggregate_uuid: str = ""
    capacity_used_allocation_units_count: int = 0
    capacity_used_allocation_units_current_usage: int = 0
    capacity_used_allocation_units_node_name: str = ""
    capacity_used_allocation_units_node_uuid: str = ""


class OntapStoragePoolArgument(CacheModel):
    """OntapStoragePoolArgument sub-model for arguments."""

    health_unhealthy_reason_arguments_code: str = ""
    health_unhealthy_reason_arguments_message: str = ""


class OntapStoragePoolNode(CacheModel):
    """OntapStoragePoolNode sub-model for nodes."""

    nodes_name: str = ""
    nodes_uuid: str = ""


class OntapStoragePool(CacheModel):
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
