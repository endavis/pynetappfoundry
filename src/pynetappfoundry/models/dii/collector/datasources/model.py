# ruff: noqa: N815
"""DiiCollectorDatasource information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiCollectorDatasourceChangeDetail(OntapModel):
    """DiiCollectorDatasourceChangeDetail sub-model for details."""

    text: str = ""
    type_: str = ""


class DiiCollectorDatasourceChange(OntapModel):
    """DiiCollectorDatasourceChange sub-model for changes."""

    summary: str = ""
    details: list[DiiCollectorDatasourceChangeDetail] = Field(default_factory=list)
    time: str = ""
    type_: str = ""


class DiiCollectorDatasourceAcquisitionunit(OntapModel):
    """DiiCollectorDatasourceAcquisitionunit sub-model for acquisitionUnit."""

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


class DiiCollectorDatasourceActivepatch(OntapModel):
    """DiiCollectorDatasourceActivepatch sub-model for activePatch."""

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


class DiiCollectorDatasourceEvent(OntapModel):
    """DiiCollectorDatasourceEvent sub-model for events."""

    statusText: str = ""
    startTime: str = ""
    numberOfTimes: int = 0
    id: int = 0
    packageName: str = ""
    endTime: str = ""
    status: str = ""


class DiiCollectorDatasourceDevice(OntapModel):
    """DiiCollectorDatasourceDevice sub-model for devices."""

    simpleName: str = ""
    ip: str = ""
    name: str = ""
    description: str = ""
    self: str = ""
    id: str = ""
    type_: str = ""
    wwn: str = ""


class DiiCollectorDatasourcePackage(OntapModel):
    """DiiCollectorDatasourcePackage sub-model for packages."""

    statusText: str = ""
    releaseStatus: str = ""
    statusCause: list[str] = Field(default_factory=list)
    packageName: str = ""
    solutionType: str = ""
    status: str = ""


class DiiCollectorDatasourceConfigPackage(OntapModel):
    """DiiCollectorDatasourceConfigPackage sub-model for packages."""

    displayName: str = ""
    attributes: str = ""
    id: str = ""
    isMandatory: bool = False


class DiiCollectorDatasourceConfig(OntapModel):
    """DiiCollectorDatasourceConfig sub-model for config."""

    vendorModelId: str = ""
    dsTypeId: str = ""
    docLink: str = ""
    vendor: str = ""
    self: str = ""
    model_: str = ""
    packages: list[DiiCollectorDatasourceConfigPackage] = Field(default_factory=list)


class DiiCollectorDatasource(OntapModel):
    """DiiCollectorDatasource information."""

    vendorModelId: str = ""
    note: str = ""
    changes: list[DiiCollectorDatasourceChange] = Field(default_factory=list)
    type_: str = ""
    lastSuccessfullyAcquiredMilliSec: int = 0
    resumeTime: str = ""
    acquisitionUnit: DiiCollectorDatasourceAcquisitionunit = Field(
        default_factory=DiiCollectorDatasourceAcquisitionunit
    )
    vendor: str = ""
    activePatch: DiiCollectorDatasourceActivepatch = Field(
        default_factory=DiiCollectorDatasourceActivepatch
    )
    model_: str = ""
    id: str = ""
    events: list[DiiCollectorDatasourceEvent] = Field(default_factory=list)
    docLink: str = ""
    resumeTimeMilliSec: int = 0
    impactIndex: int = 0
    devices: list[DiiCollectorDatasourceDevice] = Field(default_factory=list)
    packages: list[DiiCollectorDatasourcePackage] = Field(default_factory=list)
    lastSuccessfullyAcquired: str = ""
    pollStatus: str = ""
    dsTypeId: str = ""
    foundationIp: str = ""
    statusText: str = ""
    name: str = ""
    self: str = ""
    config_: DiiCollectorDatasourceConfig = Field(default_factory=DiiCollectorDatasourceConfig)
    status: str = ""
