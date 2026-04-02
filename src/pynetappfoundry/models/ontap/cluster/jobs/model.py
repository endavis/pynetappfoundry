"""OntapJob information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapJobErrorArgument(OntapModel):
    """OntapJobErrorArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapJobError(OntapModel):
    """OntapJobError sub-model for error."""

    arguments: list[OntapJobErrorArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapJobNode(OntapModel):
    """OntapJobNode sub-model for node."""

    name: str = ""


class OntapJobSvm(OntapModel):
    """OntapJobSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapJob(OntapModel):
    """OntapJob information."""

    code: int = 0
    description: str = ""
    end_time: str = ""
    error: OntapJobError = Field(default_factory=OntapJobError)
    message: str = ""
    node: OntapJobNode = Field(default_factory=OntapJobNode)
    start_time: str = ""
    state: str = ""
    svm: OntapJobSvm = Field(default_factory=OntapJobSvm)
    uuid: OntapUUID = ""
