"""OntapNetbios information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNetbiosNode(OntapModel):
    """OntapNetbiosNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNetbiosSvm(OntapModel):
    """OntapNetbiosSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNetbiosWinsServer(OntapModel):
    """OntapNetbiosWinsServer sub-model for wins_servers."""

    ip: str = ""
    state: str = ""


class OntapNetbios(OntapModel):
    """OntapNetbios information."""

    interfaces: list[str] = Field(default_factory=list)
    mode: str = ""
    name: str = ""
    name_registration_type: str = ""
    node: OntapNetbiosNode = Field(default_factory=OntapNetbiosNode)
    scope: str = ""
    state: str = ""
    suffix: str = ""
    svm: OntapNetbiosSvm = Field(default_factory=OntapNetbiosSvm)
    time_left: int = 0
    wins_servers: list[OntapNetbiosWinsServer] = Field(default_factory=list)
