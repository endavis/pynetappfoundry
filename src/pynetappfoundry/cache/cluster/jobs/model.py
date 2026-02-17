"""OntapJob information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapJobArgument(CacheModel):
    """OntapJobArgument sub-model for arguments."""

    error_arguments_code: str = ""
    error_arguments_message: str = ""


class OntapJob(CacheModel):
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
