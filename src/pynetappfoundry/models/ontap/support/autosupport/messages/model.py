"""OntapAutosupportMessage information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutosupportMessageError(OntapModel):
    """OntapAutosupportMessageError sub-model for error."""

    code: int = 0
    message: str = ""


class OntapAutosupportMessageNode(OntapModel):
    """OntapAutosupportMessageNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapAutosupportMessage(OntapModel):
    """OntapAutosupportMessage information."""

    destination: str = ""
    error: OntapAutosupportMessageError = Field(default_factory=OntapAutosupportMessageError)
    generated_on: str = ""
    index: int = 0
    message: str = ""
    node: OntapAutosupportMessageNode = Field(default_factory=OntapAutosupportMessageNode)
    state: str = ""
    subject: str = ""
    type_: str = ""
    uri: str = ""
