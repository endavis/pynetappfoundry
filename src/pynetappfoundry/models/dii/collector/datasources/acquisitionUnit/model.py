# ruff: noqa: N815
"""DiiCollectorDatasourcesAcquisitionunit information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiCollectorDatasourcesAcquisitionunitChangeDetail(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitChangeDetail sub-model for details."""

    text: str = ""
    type_: str = ""


class DiiCollectorDatasourcesAcquisitionunitChange(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitChange sub-model for changes."""

    summary: str = ""
    details: list[DiiCollectorDatasourcesAcquisitionunitChangeDetail] = Field(default_factory=list)
    time: str = ""
    type_: str = ""


class DiiCollectorDatasourcesAcquisitionunitAcquisitionunit(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitAcquisitionunit sub-model for acquisitionUnit."""

    auVersion: str = ""
    versionToBeUpgradedTo: str = ""
    isPinned: bool = False
    ip: str = ""
    auUpgradeToImageUploadedTime: int = 0
    restartRequestTime: int = 0
    upgradeOverDueMessage: str = ""
    type_: str = ""
    uuid: str = ""
    leasePeriod: int = 0
    upgradeOverDue: bool = False
    name: str = ""
    upgradeType: str = ""
    self: str = ""
    id: str = ""
    nextLeaseRenewal: int = 0
    status: str = ""


class DiiCollectorDatasourcesAcquisitionunitActivepatch(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitActivepatch sub-model for activePatch."""

    minPatchVersion: str = ""
    createTime: int = 0
    dataSourceTypeId: int = 0
    tenantId: str = ""
    name: str = ""
    description: str = ""
    endTime: int = 0
    version: str = ""
    patchReadme: str = ""
    metadataVersion: str = ""


class DiiCollectorDatasourcesAcquisitionunitEvent(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitEvent sub-model for events."""

    statusText: str = ""
    startTime: str = ""
    numberOfTimes: int = 0
    id: int = 0
    packageName: str = ""
    endTime: str = ""
    status: str = ""


class DiiCollectorDatasourcesAcquisitionunitDevice(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitDevice sub-model for devices."""

    simpleName: str = ""
    ip: str = ""
    name: str = ""
    description: str = ""
    self: str = ""
    id: str = ""
    type_: str = ""
    wwn: str = ""


class DiiCollectorDatasourcesAcquisitionunitPackage(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitPackage sub-model for packages."""

    statusText: str = ""
    releaseStatus: str = ""
    statusCause: list[str] = Field(default_factory=list)
    packageName: str = ""
    solutionType: str = ""
    status: str = ""


class DiiCollectorDatasourcesAcquisitionunitConfigPackage(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitConfigPackage sub-model for packages."""

    displayName: str = ""
    attributes: str = ""
    id: str = ""
    isMandatory: bool = False


class DiiCollectorDatasourcesAcquisitionunitConfig(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunitConfig sub-model for config."""

    vendorModelId: str = ""
    dsTypeId: str = ""
    docLink: str = ""
    vendor: str = ""
    self: str = ""
    model_: str = ""
    packages: list[DiiCollectorDatasourcesAcquisitionunitConfigPackage] = Field(
        default_factory=list
    )


class DiiCollectorDatasourcesAcquisitionunit(OntapModel):
    """DiiCollectorDatasourcesAcquisitionunit information."""

    vendorModelId: str = ""
    note: str = ""
    changes: list[DiiCollectorDatasourcesAcquisitionunitChange] = Field(default_factory=list)
    type_: str = ""
    lastSuccessfullyAcquiredMilliSec: int = 0
    resumeTime: str = ""
    acquisitionUnit: DiiCollectorDatasourcesAcquisitionunitAcquisitionunit = Field(
        default_factory=DiiCollectorDatasourcesAcquisitionunitAcquisitionunit
    )
    vendor: str = ""
    activePatch: DiiCollectorDatasourcesAcquisitionunitActivepatch = Field(
        default_factory=DiiCollectorDatasourcesAcquisitionunitActivepatch
    )
    model_: str = ""
    id: str = ""
    events: list[DiiCollectorDatasourcesAcquisitionunitEvent] = Field(default_factory=list)
    docLink: str = ""
    resumeTimeMilliSec: int = 0
    impactIndex: int = 0
    devices: list[DiiCollectorDatasourcesAcquisitionunitDevice] = Field(default_factory=list)
    packages: list[DiiCollectorDatasourcesAcquisitionunitPackage] = Field(default_factory=list)
    lastSuccessfullyAcquired: str = ""
    pollStatus: str = ""
    dsTypeId: str = ""
    foundationIp: str = ""
    statusText: str = ""
    name: str = ""
    self: str = ""
    config_: DiiCollectorDatasourcesAcquisitionunitConfig = Field(
        default_factory=DiiCollectorDatasourcesAcquisitionunitConfig
    )
    status: str = ""
