# ruff: noqa: N815
"""DiiAssetsStoragepoolsInternalvolume information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragepoolsInternalvolumeCapacity(OntapModel):
    """DiiAssetsStoragepoolsInternalvolumeCapacity sub-model for capacity."""

    compressionSavings: str = ""
    description: str = ""
    isDedupeEnabled: bool = False
    used: str = ""
    isCompressionEnabled: bool = False
    unitType: str = ""
    total: str = ""
    provisioned: str = ""
    usedRatio: str = ""
    isThinProvisioned: bool = False
    dedupeSavings: str = ""
    isThinProvisioningSupported: bool = False
    rawToUsableRatio: float = 0.0


class DiiAssetsStoragepoolsInternalvolumePerformance(OntapModel):
    """DiiAssetsStoragepoolsInternalvolumePerformance sub-model for performance."""

    snapshotCapacityTimeToFull: str = ""
    latency: str = ""
    history: list[str] = Field(default_factory=list)
    snapshotCapacityRatio: str = ""
    capacity: str = ""
    cloneSavedCapacity: str = ""
    otherCapacity: str = ""
    snapshotCapacity: str = ""
    timeToFull: str = ""
    writePending: str = ""
    dataCapacity: str = ""
    iops: str = ""
    throughput: str = ""
    ioDensity: str = ""
    capacityRatio: str = ""


class DiiAssetsStoragepoolsInternalvolume(OntapModel):
    """DiiAssetsStoragepoolsInternalvolume information."""

    spaceGuarantee: str = ""
    quotas: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    type_: str = ""
    uuid: str = ""
    capacity: DiiAssetsStoragepoolsInternalvolumeCapacity = Field(
        default_factory=DiiAssetsStoragepoolsInternalvolumeCapacity
    )
    shares: list[str] = Field(default_factory=list)
    lastSnapshotTime: str = ""
    id: int = 0
    storagePool: str = ""
    flashPoolEligibility: str = ""
    dataStores: list[str] = Field(default_factory=list)
    replicaSources: list[str] = Field(default_factory=list)
    volumes: list[str] = Field(default_factory=list)
    virtualStorage: str = ""
    qtrees: list[str] = Field(default_factory=list)
    performance: DiiAssetsStoragepoolsInternalvolumePerformance = Field(
        default_factory=DiiAssetsStoragepoolsInternalvolumePerformance
    )
    storageVirtualMachine: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    paths: list[str] = Field(default_factory=list)
    snapshotCount: int = 0
    name: str = ""
    computeResources: list[str] = Field(default_factory=list)
    isThinProvisioned: bool = False
    storageNodes: list[str] = Field(default_factory=list)
    resourceType: str = ""
    applications: list[str] = Field(default_factory=list)
    status: str = ""
