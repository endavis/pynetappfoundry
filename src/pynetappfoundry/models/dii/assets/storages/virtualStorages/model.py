# ruff: noqa: N815
"""DiiAssetsStoragesVirtualstorage information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragesVirtualstorage(OntapModel):
    """DiiAssetsStoragesVirtualstorage information."""

    disks: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    isActive: bool = False
    ports: list[str] = Field(default_factory=list)
    capacity: str = ""
    shares: list[str] = Field(default_factory=list)
    storageVirtualMachines: list[str] = Field(default_factory=list)
    vendor: str = ""
    model_: str = ""
    managementUrl: str = ""
    id: int = 0
    protocols: list[str] = Field(default_factory=list)
    virtualStorages: list[str] = Field(default_factory=list)
    microcodeVersion: str = ""
    internalVolumes: list[str] = Field(default_factory=list)
    serialNumber: str = ""
    backendStorages: list[str] = Field(default_factory=list)
    ip: str = ""
    storageResources: list[str] = Field(default_factory=list)
    volumes: list[str] = Field(default_factory=list)
    monitoring: str = ""
    zones: list[str] = Field(default_factory=list)
    qtrees: list[str] = Field(default_factory=list)
    performance: str = ""
    risks: list[str] = Field(default_factory=list)
    storagePools: list[str] = Field(default_factory=list)
    datasources: list[str] = Field(default_factory=list)
    virtualizedType: str = ""
    simpleName: str = ""
    createTime: str = ""
    paths: list[str] = Field(default_factory=list)
    name: str = ""
    naturalKey: str = ""
    storageNodes: list[str] = Field(default_factory=list)
    family: str = ""
    applications: list[str] = Field(default_factory=list)
