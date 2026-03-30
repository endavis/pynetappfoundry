"""OntapNdmpNode information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNdmpNode(OntapModel):
    """OntapNdmpNode information."""

    authentication_types: list[str] = Field(default_factory=list)
    enabled: bool = False
    node_name: str = ""
    node_uuid: str = ""
    password: str = ""
    user: str = ""
