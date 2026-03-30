"""OntapIpspace information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapIpspace(OntapModel):
    """OntapIpspace information."""

    name: str = ""
    uuid: str = ""
