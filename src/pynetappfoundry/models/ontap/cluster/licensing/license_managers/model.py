"""OntapLicenseManagerResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapLicenseManagerResponse(OntapModel):
    """OntapLicenseManagerResponse information."""

    default: bool = False
    uri_host: str = ""
    uuid: OntapUUID = ""
