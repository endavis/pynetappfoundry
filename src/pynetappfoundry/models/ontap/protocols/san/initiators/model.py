"""OntapInitiator information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapInitiatorSvm(OntapModel):
    """OntapInitiatorSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapInitiator(OntapModel):
    """OntapInitiator information."""

    comment: str = ""
    name: str = ""
    protocol: str = ""
    svm: OntapInitiatorSvm = Field(default_factory=OntapInitiatorSvm)
