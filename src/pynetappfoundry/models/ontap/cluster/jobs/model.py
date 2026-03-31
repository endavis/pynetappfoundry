"""OntapJob information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapJobArgument(OntapModel):
    """OntapJobArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapJob(OntapModel):
    """OntapJob information."""

    code: int = 0
    description: str = ""
    end_time: str = ""
    error_arguments: list[OntapJobArgument] = Field(default_factory=list)
    error_code: str = ""
    error_message: str = ""
    message: str = ""
    node_name: str = ""
    start_time: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: OntapUUID = ""
