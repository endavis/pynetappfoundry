"""OntapCoredump information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCoredumpNode(OntapModel):
    """OntapCoredumpNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCoredump(OntapModel):
    """OntapCoredump information."""

    is_partial: bool = False
    is_saved: bool = False
    md5_data_checksum: str = ""
    name: str = ""
    node: OntapCoredumpNode = Field(default_factory=OntapCoredumpNode)
    panic_time: str = ""
    size: int = 0
    type_: str = ""
