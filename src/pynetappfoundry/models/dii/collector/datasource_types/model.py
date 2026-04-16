# ruff: noqa: E501, N815
"""DiiCollectorDatasourceType information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiCollectorDatasourceTypePackageAttribute(OntapModel):
    """DiiCollectorDatasourceTypePackageAttribute sub-model for attributes."""

    role: str = ""
    guiorder: int = 0
    minValueFromString: str = ""
    level: str = ""
    listensToTriggers: str = ""
    defaultValue: str = ""
    maxValue: str = ""
    triggersClearing: bool = False
    description: str = ""
    label: str = ""
    type_: str = ""
    bulkEditable: bool = False
    isHidden: bool = False
    enums: list[str] = Field(default_factory=list)
    minValue: str = ""
    isAdvanced: bool = False
    isEditable: bool = False
    isCloneable: bool = False
    maxValueFromString: str = ""
    isEncrypted: bool = False
    name: str = ""
    defaultValueFromString: str = ""
    value: str = ""
    isMandatory: bool = False


class DiiCollectorDatasourceTypePackage(OntapModel):
    """DiiCollectorDatasourceTypePackage sub-model for packages."""

    displayName: str = ""
    attributes: list[DiiCollectorDatasourceTypePackageAttribute] = Field(default_factory=list)
    id: str = ""
    mandatory: bool = False
    isMandatory: bool = False


class DiiCollectorDatasourceTypeVendormodelDatasourcetypevendormodelid(OntapModel):
    """DiiCollectorDatasourceTypeVendormodelDatasourcetypevendormodelid sub-model for dataSourceTypeVendorModelId."""

    dsTypeId: int = 0
    id: int = 0


class DiiCollectorDatasourceTypeVendormodel(OntapModel):
    """DiiCollectorDatasourceTypeVendormodel sub-model for vendorModels."""

    modelDescription: str = ""
    modelName: str = ""
    docLink: str = ""
    imageURL: str = ""
    id: str = ""
    vendorName: str = ""
    dataSourceTypeVendorModelId: DiiCollectorDatasourceTypeVendormodelDatasourcetypevendormodelid = Field(
        default_factory=DiiCollectorDatasourceTypeVendormodelDatasourcetypevendormodelid
    )


class DiiCollectorDatasourceType(OntapModel):
    """DiiCollectorDatasourceType information."""

    name: str = ""
    description: str = ""
    self: str = ""
    id: str = ""
    type_: str = ""
    packages: list[DiiCollectorDatasourceTypePackage] = Field(default_factory=list)
    vendorModels: list[DiiCollectorDatasourceTypeVendormodel] = Field(default_factory=list)
