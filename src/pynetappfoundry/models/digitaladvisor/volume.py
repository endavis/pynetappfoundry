# The field names are the GraphQL camelCase names, so filter paths equal API paths.
# ruff: noqa: N815
"""Digital Advisor volume model: the curated scalars and nested objects, no personal data."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DigitalAdvisorVserver(OntapModel):
    """The ``Vserver`` scalar fields."""

    id: str | None = None
    name: str | None = None
    type: str | None = None
    subType: str | None = None


class DigitalAdvisorAggregate(OntapModel):
    """The ``Aggregate`` scalar fields."""

    id: str | None = None
    name: str | None = None
    systemSerialNumber: str | None = None
    raidType: str | None = None
    storageType: str | None = None
    isRoot: bool | None = None
    snapLockMode: str | None = None
    tieredKB: float | None = None
    tieringProvider: str | None = None
    isFabricPoolEnabled: bool | None = None


class DigitalAdvisorVolumeCapacity(OntapModel):
    """The ``VolumeCapacity`` scalar fields."""

    usableKB: float | None = None
    usableKiB: float | None = None
    usedKB: float | None = None
    usedKiB: float | None = None
    availableKB: float | None = None
    inactiveKB: float | None = None
    sizeKB: float | None = None
    reportedOn: str | None = None


class DigitalAdvisorVolumeProvisioning(OntapModel):
    """The ``VolumeProvisioning`` fields."""

    isThinProvisioned: bool | None = None
    type: str | None = None
    style: str | None = None
    extendedStyle: str | None = None
    language: str | None = None


class DigitalAdvisorVolumePerformance(OntapModel):
    """The ``VolumePerformance`` fields."""

    iops: float | None = None
    averageLatencyMs: float | None = None


class DigitalAdvisorVolumeFiles(OntapModel):
    """The ``VolumeFiles`` fields."""

    total: float | None = None
    used: float | None = None


class DigitalAdvisorVolumeSystemRef(OntapModel):
    """A scalar-only reference to the system that holds the volume."""

    systemId: str | None = None
    serialNumber: str | None = None
    hostName: str | None = None


class DigitalAdvisorVolume(OntapModel):
    """An Active IQ Digital Advisor volume."""

    id: str | None = None
    name: str | None = None
    instanceUUID: str | None = None
    state: str | None = None
    tieringPolicy: str | None = None
    autoSizeMode: str | None = None
    snapLockMode: str | None = None
    snapshotCount: float | None = None
    usedCapacityPercentage: float | None = None
    isRoot: bool | None = None
    isEncrypted: bool | None = None
    isAutoSizeEnabled: bool | None = None
    isARPEnabled: bool | None = None
    protocols: list[str] | None = None
    enabledEfficiencyFeatures: list[str] | None = None
    tieringMinimumCoolingDays: float | None = None
    snapshotReserveUsedPercentage: float | None = None
    qosPolicyGroup: str | None = None
    vserver: DigitalAdvisorVserver | None = None
    aggregate: DigitalAdvisorAggregate | None = None
    capacity: DigitalAdvisorVolumeCapacity | None = None
    provisioning: DigitalAdvisorVolumeProvisioning | None = None
    performanceSummary: DigitalAdvisorVolumePerformance | None = None
    files: DigitalAdvisorVolumeFiles | None = None
    system: DigitalAdvisorVolumeSystemRef | None = None
