"""OntapAntiRansomware information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapAntiRansomware(OntapModel):
    """OntapAntiRansomware information."""

    name: str = ""
    version: str = ""
