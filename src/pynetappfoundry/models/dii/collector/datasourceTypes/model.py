# ruff: noqa: E501, N815
"""DiiCollectorDatasourceTypes information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiCollectorDatasourceTypesPackageAttribute(OntapModel):
    """DiiCollectorDatasourceTypesPackageAttribute sub-model for attributes."""

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


class DiiCollectorDatasourceTypesPackage(OntapModel):
    """DiiCollectorDatasourceTypesPackage sub-model for packages."""

    displayName: str = ""
    attributes: list[DiiCollectorDatasourceTypesPackageAttribute] = Field(default_factory=list)
    id: str = ""
    mandatory: bool = False
    isMandatory: bool = False


class DiiCollectorDatasourceTypesVendormodelDatasourcetypevendormodelid(OntapModel):
    """DiiCollectorDatasourceTypesVendormodelDatasourcetypevendormodelid sub-model for dataSourceTypeVendorModelId."""

    dsTypeId: int = 0
    id: int = 0


class DiiCollectorDatasourceTypesVendormodel(OntapModel):
    """DiiCollectorDatasourceTypesVendormodel sub-model for vendorModels."""

    modelDescription: str = ""
    modelName: str = ""
    docLink: str = ""
    imageURL: str = ""
    id: str = ""
    vendorName: str = ""
    dataSourceTypeVendorModelId: DiiCollectorDatasourceTypesVendormodelDatasourcetypevendormodelid = Field(
        default_factory=DiiCollectorDatasourceTypesVendormodelDatasourcetypevendormodelid
    )


class DiiCollectorDatasourceTypes(OntapModel):
    """DiiCollectorDatasourceTypes information."""

    name: str = ""
    description: str = ""
    self: str = ""
    id: str = ""
    type_: str = ""
    packages: list[DiiCollectorDatasourceTypesPackage] = Field(default_factory=list)
    vendorModels: list[DiiCollectorDatasourceTypesVendormodel] = Field(default_factory=list)
