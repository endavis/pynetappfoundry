"""OntapLicenseManagerResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapLicenseManagerResponseUri(OntapModel):
    """OntapLicenseManagerResponseUri sub-model for uri."""

    host: str = ""


class OntapLicenseManagerResponse(OntapModel):
    """OntapLicenseManagerResponse information."""

    default: bool = False
    uri: OntapLicenseManagerResponseUri = Field(default_factory=OntapLicenseManagerResponseUri)
    uuid: OntapUUID = ""
