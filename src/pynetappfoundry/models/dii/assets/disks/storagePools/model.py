# ruff: noqa: N815
"""DiiAssetsDisksStoragepool information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsDisksStoragepool(OntapModel):
    """DiiAssetsDisksStoragepool information."""

    usesFlashPools: bool = False
    internalVolumes: list[str] = Field(default_factory=list)
    disks: list[str] = Field(default_factory=list)
    minDiskType: str = ""
    vendorTier: str = ""
    storageResources: list[str] = Field(default_factory=list)
    volumes: list[str] = Field(default_factory=list)
    isAutoTiering: bool = False
    minDiskSpeed: int = 0
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    type_: str = ""
    capacity: str = ""
    isRaidGroup: bool = False
    performance: str = ""
    datasources: list[str] = Field(default_factory=list)
    storageVirtualMachines: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    storageNodes: list[str] = Field(default_factory=list)
    id: int = 0
    redundancy: str = ""
    isVirtual: bool = False
    minDiskSize: str = ""
