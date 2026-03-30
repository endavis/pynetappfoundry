"""OntapResourceTag information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapResourceTag(OntapModel):
    """OntapResourceTag information."""

    num_resources: int = 0
    value: str = ""
