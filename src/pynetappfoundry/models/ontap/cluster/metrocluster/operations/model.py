"""OntapMetroclusterOperation information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMetroclusterOperation(OntapModel):
    """OntapMetroclusterOperation information."""

    additional_info: str = ""
    command_line: str = ""
    end_time: str = ""
    errors: list[str] = Field(default_factory=list)
    node_name: str = ""
    node_uuid: str = ""
    start_time: str = ""
    state: str = ""
    type_: str = ""
    uuid: str = ""
