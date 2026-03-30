"""OntapSupportedAlgorithms information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSupportedAlgorithms(OntapModel):
    """OntapSupportedAlgorithms information."""

    algorithm_id: int = 0
    algorithm_name: str = ""
    algorithm_type: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    scope: str = ""
