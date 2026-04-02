"""OntapNdmpNode information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNdmpNodeNode(OntapModel):
    """OntapNdmpNodeNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNdmpNode(OntapModel):
    """OntapNdmpNode information."""

    authentication_types: list[str] = Field(default_factory=list)
    enabled: bool = False
    node: OntapNdmpNodeNode = Field(default_factory=OntapNdmpNodeNode)
    password: str = ""
    user: str = ""
