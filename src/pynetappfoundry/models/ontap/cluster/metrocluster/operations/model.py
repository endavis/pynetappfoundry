"""OntapMetroclusterOperation information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMetroclusterOperationNode(OntapModel):
    """OntapMetroclusterOperationNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterOperation(OntapModel):
    """OntapMetroclusterOperation information."""

    additional_info: str = ""
    command_line: str = ""
    end_time: str = ""
    errors: list[str] = Field(default_factory=list)
    node: OntapMetroclusterOperationNode = Field(default_factory=OntapMetroclusterOperationNode)
    start_time: str = ""
    state: str = ""
    type_: str = ""
    uuid: str = ""
