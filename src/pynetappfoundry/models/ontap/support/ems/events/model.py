"""OntapEmsEventResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsEventResponseParameter(OntapModel):
    """OntapEmsEventResponseParameter sub-model for parameters."""

    name: str = ""
    value: str = ""


class OntapEmsEventResponse(OntapModel):
    """OntapEmsEventResponse information."""

    index: int = 0
    log_message: str = ""
    message_name: str = ""
    message_severity: str = ""
    node_name: str = ""
    node_uuid: str = ""
    parameters: list[OntapEmsEventResponseParameter] = Field(default_factory=list)
    source: str = ""
    time: str = ""
