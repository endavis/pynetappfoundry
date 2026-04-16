# ruff: noqa: N815
"""DiiAssetsIscsisessionsTargetvolume information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsIscsisessionsTargetvolumeCapacity(OntapModel):
    """DiiAssetsIscsisessionsTargetvolumeCapacity sub-model for capacity."""

    unitType: str = ""
    total: str = ""
    usedRatio: str = ""
    description: str = ""
    isThinProvisioned: bool = False
    raw: str = ""
    used: str = ""
    written: str = ""


class DiiAssetsIscsisessionsTargetvolumePerformance(OntapModel):
    """DiiAssetsIscsisessionsTargetvolumePerformance sub-model for performance."""

    latency: str = ""
    history: list[str] = Field(default_factory=list)
    capacity: str = ""
    cacheHitRatio: str = ""
    iscsi: str = ""
    timeToFull: str = ""
    writePending: str = ""
    iops: str = ""
    throughput: str = ""
    ioDensity: str = ""
    fc: str = ""
    partialBlocksRatio: str = ""
    capacityRatio: str = ""


class DiiAssetsIscsisessionsTargetvolume(OntapModel):
    """DiiAssetsIscsisessionsTargetvolume information."""

    virtualizer: str = ""
    isAutoTiering: bool = False
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    type_: str = ""
    ports: list[str] = Field(default_factory=list)
    uuid: str = ""
    capacity: DiiAssetsIscsisessionsTargetvolumeCapacity = Field(
        default_factory=DiiAssetsIscsisessionsTargetvolumeCapacity
    )
    diskGroup: str = ""
    id: int = 0
    dataStores: list[str] = Field(default_factory=list)
    virtualStoragePools: list[str] = Field(default_factory=list)
    isReplicaTarget: bool = False
    qtree: str = ""
    isMainframe: bool = False
    protectionType: str = ""
    replicaSources: list[str] = Field(default_factory=list)
    isMeta: bool = False
    label: str = ""
    internalVolume: str = ""
    virtualStorageResources: list[str] = Field(default_factory=list)
    autoTierPolicy: str = ""
    performance: DiiAssetsIscsisessionsTargetvolumePerformance = Field(
        default_factory=DiiAssetsIscsisessionsTargetvolumePerformance
    )
    storageVirtualMachine: str = ""
    storagePools: list[str] = Field(default_factory=list)
    virtualizedType: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    paths: list[str] = Field(default_factory=list)
    name: str = ""
    computeResources: list[str] = Field(default_factory=list)
    isThinProvisioned: bool = False
    isReplicaSource: bool = False
    storageNodes: list[str] = Field(default_factory=list)
    isVirtual: bool = False
    isSnapshot: bool = False
    resourceType: str = ""
    applications: list[str] = Field(default_factory=list)
