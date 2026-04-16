# ruff: noqa: N815
"""DiiAssetsVirtualmachine information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVirtualmachinePerformance(OntapModel):
    """DiiAssetsVirtualmachinePerformance sub-model for performance."""

    cpuUtilization: str = ""
    diskThroughput: str = ""
    swapRate: str = ""
    diskIops: str = ""
    diskLatency: str = ""
    optimization: str = ""
    memoryUtilization: str = ""
    history: list[str] = Field(default_factory=list)
    ipThroughput: str = ""
    capacity: str = ""
    capacityRatio: str = ""


class DiiAssetsVirtualmachine(OntapModel):
    """DiiAssetsVirtualmachine information."""

    memory: str = ""
    vmdks: list[str] = Field(default_factory=list)
    guestState: str = ""
    dnsName: str = ""
    annotations: list[str] = Field(default_factory=list)
    processors: int = 0
    ports: list[str] = Field(default_factory=list)
    capacity: str = ""
    powerState: str = ""
    fileSystems: list[str] = Field(default_factory=list)
    host: str = ""
    id: int = 0
    os: str = ""
    ip: str = ""
    storageResources: list[str] = Field(default_factory=list)
    zones: list[str] = Field(default_factory=list)
    powerStateChangeTime: str = ""
    performance: DiiAssetsVirtualmachinePerformance = Field(
        default_factory=DiiAssetsVirtualmachinePerformance
    )
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    createTime: str = ""
    paths: list[str] = Field(default_factory=list)
    name: str = ""
    dataStore: str = ""
    resourceType: str = ""
    applications: list[str] = Field(default_factory=list)
