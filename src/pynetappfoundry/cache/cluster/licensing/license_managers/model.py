"""OntapLicenseManagerResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapLicenseManagerResponse(CacheModel):
    """OntapLicenseManagerResponse information."""

    default: bool = False
    uri_host: str = ""
    uuid: OntapUUID = ""
