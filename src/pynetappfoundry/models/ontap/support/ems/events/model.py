"""OntapEmsEventResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsEventResponseMessage(OntapModel):
    """OntapEmsEventResponseMessage sub-model for message."""

    name: str = ""
    severity: str = ""


class OntapEmsEventResponseNode(OntapModel):
    """OntapEmsEventResponseNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapEmsEventResponseParameter(OntapModel):
    """OntapEmsEventResponseParameter sub-model for parameters."""

    name: str = ""
    value: str = ""


class OntapEmsEventResponse(OntapModel):
    """OntapEmsEventResponse information."""

    index: int = 0
    log_message: str = ""
    message: OntapEmsEventResponseMessage = Field(default_factory=OntapEmsEventResponseMessage)
    node: OntapEmsEventResponseNode = Field(default_factory=OntapEmsEventResponseNode)
    parameters: list[OntapEmsEventResponseParameter] = Field(default_factory=list)
    source: str = ""
    time: str = ""
