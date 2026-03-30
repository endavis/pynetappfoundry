"""OntapSoftwarePackageDownloadGet information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSoftwarePackageDownloadGet(OntapModel):
    """OntapSoftwarePackageDownloadGet information."""

    code: int = 0
    message: str = ""
    state: str = ""
