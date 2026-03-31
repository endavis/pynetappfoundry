"""OntapLicensePackageResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLicensePackageResponseLicense(OntapModel):
    """OntapLicensePackageResponseLicense sub-model for licenses."""

    active: bool = False
    capacity_maximum_size: int = 0
    capacity_used_size: int = 0
    compliance_state: str = ""
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
    entitlement_action: str = ""
    entitlement_risk: str = ""
    keys: list[str] = Field(default_factory=list)
    licenses: list[OntapLicensePackageResponseLicense] = Field(default_factory=list)
    name: str = ""
    scope: str = ""
    state: str = ""
