"""OntapLicensePackageResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLicensePackageResponseEntitlement(OntapModel):
    """OntapLicensePackageResponseEntitlement sub-model for entitlement."""

    action: str = ""
    risk: str = ""


class OntapLicensePackageResponseLicenseCapacity(OntapModel):
    """OntapLicensePackageResponseLicenseCapacity sub-model for capacity."""

    maximum_size: int = 0
    used_size: int = 0


class OntapLicensePackageResponseLicenseCompliance(OntapModel):
    """OntapLicensePackageResponseLicenseCompliance sub-model for compliance."""

    state: str = ""


class OntapLicensePackageResponseLicense(OntapModel):
    """OntapLicensePackageResponseLicense sub-model for licenses."""

    active: bool = False
    capacity: OntapLicensePackageResponseLicenseCapacity = Field(
        default_factory=OntapLicensePackageResponseLicenseCapacity
    )
    compliance: OntapLicensePackageResponseLicenseCompliance = Field(
        default_factory=OntapLicensePackageResponseLicenseCompliance
    )
    evaluation: bool = False
    expiry_time: str = ""
    host_id: str = ""
    installed_license: str = ""
    owner: str = ""
    serial_number: str = ""
    shutdown_imminent: bool = False
    start_time: str = ""


class OntapLicensePackageResponse(OntapModel):
    """OntapLicensePackageResponse information."""

    description: str = ""
    entitlement: OntapLicensePackageResponseEntitlement = Field(
        default_factory=OntapLicensePackageResponseEntitlement
    )
    keys: list[str] = Field(default_factory=list)
    licenses: list[OntapLicensePackageResponseLicense] = Field(default_factory=list)
    name: str = ""
    scope: str = ""
    state: str = ""
