"""OntapSoftwarePackageDownloadGet information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSoftwarePackageDownloadGet(CacheModel):
    """OntapSoftwarePackageDownloadGet information."""

    code: int = 0
    message: str = ""
    state: str = ""
