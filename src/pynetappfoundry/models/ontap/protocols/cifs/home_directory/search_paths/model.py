"""OntapCifsSearchPath information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapCifsSearchPath(OntapModel):
    """OntapCifsSearchPath information."""

    index: int = 0
    path: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
