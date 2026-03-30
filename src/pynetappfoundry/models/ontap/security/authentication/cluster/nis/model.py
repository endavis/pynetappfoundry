"""OntapClusterNisService information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapClusterNisService(OntapModel):
    """OntapClusterNisService information."""

    server: str = ""
    status_code: str = ""
    status_message: str = ""
