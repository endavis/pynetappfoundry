"""OntapInitiator information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapInitiator(OntapModel):
    """OntapInitiator information."""

    comment: str = ""
    name: str = ""
    protocol: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
