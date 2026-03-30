"""OntapSoftwarePackage information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSoftwarePackage(OntapModel):
    """OntapSoftwarePackage information."""

    create_time: str = ""
    version: str = ""
