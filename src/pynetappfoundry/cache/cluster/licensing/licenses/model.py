"""OntapLicensePackageResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLicensePackageResponseLicense(CacheModel):
    """OntapLicensePackageResponseLicense sub-model for licenses."""

    licenses_active: bool = False
    licenses_capacity_maximum_size: int = 0
    licenses_capacity_used_size: int = 0
    licenses_compliance_state: str = ""
    licenses_evaluation: bool = False
    licenses_expiry_time: str = ""
    licenses_host_id: str = ""
    licenses_installed_license: str = ""
    licenses_owner: str = ""
    licenses_serial_number: str = ""
    licenses_shutdown_imminent: bool = False
    licenses_start_time: str = ""


class OntapLicensePackageResponse(CacheModel):
    """OntapLicensePackageResponse information."""

    description: str = ""
    entitlement_action: str = ""
    entitlement_risk: str = ""
    keys: list[str] = Field(default_factory=list)
    licenses: list[OntapLicensePackageResponseLicense] = Field(default_factory=list)
    name: str = ""
    scope: str = ""
    state: str = ""
