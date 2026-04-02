"""OntapStoragePool information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStoragePoolCapacityDiskDisk(OntapModel):
    """OntapStoragePoolCapacityDiskDisk sub-model for disk."""

    name: str = ""


class OntapStoragePoolCapacityDisk(OntapModel):
    """OntapStoragePoolCapacityDisk sub-model for disks."""

    disk: OntapStoragePoolCapacityDiskDisk = Field(default_factory=OntapStoragePoolCapacityDiskDisk)
    total_size: int = 0
    usable_size: int = 0


class OntapStoragePoolCapacitySpareAllocationUnitNode(OntapModel):
    """OntapStoragePoolCapacitySpareAllocationUnitNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapStoragePoolCapacitySpareAllocationUnit(OntapModel):
    """OntapStoragePoolCapacitySpareAllocationUnit sub-model for spare_allocation_units."""

    available_size: int = 0
    count: int = 0
    node: OntapStoragePoolCapacitySpareAllocationUnitNode = Field(
        default_factory=OntapStoragePoolCapacitySpareAllocationUnitNode
    )
    size: int = 0
    syncmirror_pool: str = ""


class OntapStoragePoolCapacityUsedAllocationUnitAggregate(OntapModel):
    """OntapStoragePoolCapacityUsedAllocationUnitAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapStoragePoolCapacityUsedAllocationUnitNode(OntapModel):
    """OntapStoragePoolCapacityUsedAllocationUnitNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapStoragePoolCapacityUsedAllocationUnit(OntapModel):
    """OntapStoragePoolCapacityUsedAllocationUnit sub-model for used_allocation_units."""

    aggregate: OntapStoragePoolCapacityUsedAllocationUnitAggregate = Field(
        default_factory=OntapStoragePoolCapacityUsedAllocationUnitAggregate
    )
    count: int = 0
    current_usage: int = 0
    node: OntapStoragePoolCapacityUsedAllocationUnitNode = Field(
        default_factory=OntapStoragePoolCapacityUsedAllocationUnitNode
    )


class OntapStoragePoolCapacity(OntapModel):
    """OntapStoragePoolCapacity sub-model for capacity."""

    disk_count: int = 0
    disks: list[OntapStoragePoolCapacityDisk] = Field(default_factory=list)
    remaining: int = 0
    spare_allocation_units: list[OntapStoragePoolCapacitySpareAllocationUnit] = Field(
        default_factory=list
    )
    total: int = 0
    used_allocation_units: list[OntapStoragePoolCapacityUsedAllocationUnit] = Field(
        default_factory=list
    )


class OntapStoragePoolHealthUnhealthyReasonArgument(OntapModel):
    """OntapStoragePoolHealthUnhealthyReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapStoragePoolHealthUnhealthyReason(OntapModel):
    """OntapStoragePoolHealthUnhealthyReason sub-model for unhealthy_reason."""

    arguments: list[OntapStoragePoolHealthUnhealthyReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapStoragePoolHealth(OntapModel):
    """OntapStoragePoolHealth sub-model for health."""

    is_healthy: bool = False
    state: str = ""
    unhealthy_reason: OntapStoragePoolHealthUnhealthyReason = Field(
        default_factory=OntapStoragePoolHealthUnhealthyReason
    )


class OntapStoragePoolNode(OntapModel):
    """OntapStoragePoolNode sub-model for nodes."""

    name: str = ""
    uuid: str = ""


class OntapStoragePool(OntapModel):
    """OntapStoragePool information."""

    capacity: OntapStoragePoolCapacity = Field(default_factory=OntapStoragePoolCapacity)
    health: OntapStoragePoolHealth = Field(default_factory=OntapStoragePoolHealth)
    name: str = ""
    nodes: list[OntapStoragePoolNode] = Field(default_factory=list)
    storage_type: str = ""
    uuid: str = ""
