# The field names are the GraphQL camelCase names, so filter paths equal API paths.
# ruff: noqa: N815
"""Digital Advisor system model: the curated scalars and nested objects, no personal data.

The contact people (``contactPerson``, ``salesRepresentative``, ``csm``,
``retentionSpecialist``, ``solutionEngineerSpecialist``, ``sam``) and a site's street
address and postal code are deliberately absent; the backend refuses to select them
(ADR-0037).
"""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DigitalAdvisorSite(OntapModel):
    """The ``Site`` fields without the address lines and postal code."""

    id: str | None = None
    cmatId: str | None = None
    name: str | None = None
    countryCode: str | None = None
    city: str | None = None
    state: str | None = None


class DigitalAdvisorCustomer(OntapModel):
    """The ``Customer`` scalar fields."""

    id: str | None = None
    cmatId: str | None = None
    name: str | None = None


class DigitalAdvisorNagp(OntapModel):
    """The ``Nagp`` fields."""

    id: str | None = None
    name: str | None = None


class DigitalAdvisorHardwareModel(OntapModel):
    """The ``HardwareModel`` fields."""

    name: str | None = None
    modelRevision: str | None = None
    endOfAvailability: str | None = None
    endOfSupport: str | None = None


class DigitalAdvisorContract(OntapModel):
    """The ``SystemContract`` fields."""

    softwareContractStartDate: str | None = None
    hardwareContractStartDate: str | None = None
    nrdContractStartDate: str | None = None
    expiryDate: str | None = None
    softwareContractEndDate: str | None = None
    hardwareContractEndDate: str | None = None
    nrdContractEndDate: str | None = None
    overallContractEndDate: str | None = None
    softwareContractId: str | None = None
    hardwareContractId: str | None = None
    nrdContractId: str | None = None
    isContractActive: bool | None = None
    hardwareServiceLevel: str | None = None
    hardwareWarrantyEndDate: str | None = None
    hardwareWarrantyStartDate: str | None = None


class DigitalAdvisorSoftwareVersion(OntapModel):
    """The ``SystemSoftwareVersion`` scalar fields."""

    fullVersionString: str | None = None


class DigitalAdvisorEndOfSupport(OntapModel):
    """The ``EndOfSupport`` dates."""

    earliestShelfEndOfSupportDate: str | None = None
    earliestDiskEndOfSupportDate: str | None = None
    earliestEndOfSupportDate: str | None = None
    latestPVRDate: str | None = None
    latestEndOfSupportDate: str | None = None


class DigitalAdvisorAutoSupportConfig(OntapModel):
    """The ``AutoSupportConfig`` fields the backend reads."""

    autoSupportStatus: str | None = None
    autoSupportTransport: str | None = None
    isAutoSupportOnDemandEnabled: bool | None = None
    isAutoSupportOnDemandCapable: bool | None = None


class DigitalAdvisorAutoSupport(OntapModel):
    """The ``AutoSupport`` fields of a system's latest ASUP."""

    asupId: str | None = None
    generatedDate: str | None = None
    type: str | None = None
    receivedDate: str | None = None


class DigitalAdvisorSystem(OntapModel):
    """An Active IQ Digital Advisor system."""

    systemId: str | None = None
    serialNumber: str | None = None
    systemState: str | None = None
    model: str | None = None
    productType: str | None = None
    platformType: str | None = None
    systemShipmentDate: str | None = None
    serviceTier: str | None = None
    hasPvr: bool | None = None
    supportAddOns: list[str] | None = None
    hostName: str | None = None
    osVersion: str | None = None
    osType: str | None = None
    ageInYears: int | None = None
    customerGroup: str | None = None
    recommendedOSVersion: str | None = None
    latestSalesOrder: str | None = None
    type: str | None = None
    multiArea: str | None = None
    incumbentResellerCompany: str | None = None
    techRefreshStatus: str | None = None
    hyperScalerName: str | None = None
    marketingType: str | None = None
    storageConfiguration: str | None = None
    originalShipDate: str | None = None
    operationalDate: str | None = None
    lastRebootTime: str | None = None
    utcOffset: int | None = None
    isFabricPool: bool | None = None
    belongsToMixModelCluster: bool | None = None
    site: DigitalAdvisorSite | None = None
    customer: DigitalAdvisorCustomer | None = None
    nagp: DigitalAdvisorNagp | None = None
    hardwareModel: DigitalAdvisorHardwareModel | None = None
    contract: DigitalAdvisorContract | None = None
    softwareVersion: DigitalAdvisorSoftwareVersion | None = None
    endOfSupport: DigitalAdvisorEndOfSupport | None = None
    autoSupportConfig: DigitalAdvisorAutoSupportConfig | None = None
    latestAsup: DigitalAdvisorAutoSupport | None = None
