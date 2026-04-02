"""OntapCifsConnection information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsConnectionNode(OntapModel):
    """OntapCifsConnectionNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCifsConnectionSession(OntapModel):
    """OntapCifsConnectionSession sub-model for sessions."""

    identifier: int = 0


class OntapCifsConnectionSvm(OntapModel):
    """OntapCifsConnectionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsConnection(OntapModel):
    """OntapCifsConnection information."""

    client_ip: str = ""
    client_port: int = 0
    identifier: int = 0
    network_context_id: int = 0
    node: OntapCifsConnectionNode = Field(default_factory=OntapCifsConnectionNode)
    server_ip: str = ""
    sessions: list[OntapCifsConnectionSession] = Field(default_factory=list)
    svm: OntapCifsConnectionSvm = Field(default_factory=OntapCifsConnectionSvm)
