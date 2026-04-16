# ruff: noqa: N815
"""DiiAssetsHost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsHostPerformance(OntapModel):
    """DiiAssetsHostPerformance sub-model for performance."""

    cpuUtilization: str = ""
    diskThroughput: str = ""
    swapRate: str = ""
    diskIops: str = ""
    diskLatency: str = ""
    memoryUtilization: str = ""
    history: list[str] = Field(default_factory=list)
    ipThroughput: str = ""


class DiiAssetsHost(OntapModel):
    """DiiAssetsHost information."""

    memory: str = ""
    annotations: list[str] = Field(default_factory=list)
    isHypervisor: bool = False
    virtualMachines: list[str] = Field(default_factory=list)
    ports: list[str] = Field(default_factory=list)
    isActive: bool = False
    manufacturer: str = ""
    capacity: str = ""
    fileSystems: list[str] = Field(default_factory=list)
    clusterName: str = ""
    model_: str = ""
    id: int = 0
    cpuCount: int = 0
    os: str = ""
    dataCenter: str = ""
    ip: str = ""
    storageResources: list[str] = Field(default_factory=list)
    cpu: str = ""
    zones: list[str] = Field(default_factory=list)
    performance: DiiAssetsHostPerformance = Field(default_factory=DiiAssetsHostPerformance)
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    createTime: str = ""
    paths: list[str] = Field(default_factory=list)
    name: str = ""
    clusterHosts: list[str] = Field(default_factory=list)
    resourceType: str = ""
    applications: list[str] = Field(default_factory=list)
