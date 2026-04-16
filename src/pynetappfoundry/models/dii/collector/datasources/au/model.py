# ruff: noqa: E501, N815
"""DiiCollectorDatasourcesAu information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiCollectorDatasourcesAuChangeresponsDetail(OntapModel):
    """DiiCollectorDatasourcesAuChangeresponsDetail sub-model for details."""

    text: str = ""
    type_: str = ""


class DiiCollectorDatasourcesAuChangerespons(OntapModel):
    """DiiCollectorDatasourcesAuChangerespons sub-model for changeResponses."""

    summary: str = ""
    details: list[DiiCollectorDatasourcesAuChangeresponsDetail] = Field(default_factory=list)
    time: str = ""
    type_: str = ""


class DiiCollectorDatasourcesAuVendormodelDatasourcetypevendormodelid(OntapModel):
    """DiiCollectorDatasourcesAuVendormodelDatasourcetypevendormodelid sub-model for dataSourceTypeVendorModelId."""

    dsTypeId: int = 0
    id: int = 0


class DiiCollectorDatasourcesAuVendormodel(OntapModel):
    """DiiCollectorDatasourcesAuVendormodel sub-model for vendorModel."""

    modelDescription: str = ""
    modelName: str = ""
    docLink: str = ""
    imageURL: str = ""
    id: str = ""
    vendorName: str = ""
    dataSourceTypeVendorModelId: DiiCollectorDatasourcesAuVendormodelDatasourcetypevendormodelid = (
        Field(default_factory=DiiCollectorDatasourcesAuVendormodelDatasourcetypevendormodelid)
    )


class DiiCollectorDatasourcesAuAcquisitionunit(OntapModel):
    """DiiCollectorDatasourcesAuAcquisitionunit sub-model for acquisitionUnit."""

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


class DiiCollectorDatasourcesAuAttribute(OntapModel):
    """DiiCollectorDatasourcesAuAttribute sub-model for attributes."""

    dataSourceId: int = 0
    valueChanged: bool = False
    editable: bool = False
    dataSourceTypeId: int = 0
    name: str = ""
    id: int = 0
    bulkEditable: bool = False
    value: str = ""


class DiiCollectorDatasourcesAu(OntapModel):
    """DiiCollectorDatasourcesAu information."""

    lastAcquired: int = 0
    auId: int = 0
    active: bool = False
    changeResponses: list[DiiCollectorDatasourcesAuChangerespons] = Field(default_factory=list)
    type_: str = ""
    manual: int = 0
    vendorModel: DiiCollectorDatasourcesAuVendormodel = Field(
        default_factory=DiiCollectorDatasourcesAuVendormodel
    )
    resumeTime: int = 0
    acquisitionUnit: DiiCollectorDatasourcesAuAcquisitionunit = Field(
        default_factory=DiiCollectorDatasourcesAuAcquisitionunit
    )
    lastPoll: int = 0
    statusExt: str = ""
    name: str = ""
    self: str = ""
    attributes: list[DiiCollectorDatasourcesAuAttribute] = Field(default_factory=list)
    id: int = 0
    time: int = 0
    postponed: bool = False
    status: str = ""
