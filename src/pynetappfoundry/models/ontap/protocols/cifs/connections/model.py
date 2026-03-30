"""OntapCifsConnection information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsConnectionSession(OntapModel):
    """OntapCifsConnectionSession sub-model for sessions."""

    sessions_identifier: int = 0


class OntapCifsConnection(OntapModel):
    """OntapCifsConnection information."""

    client_ip: str = ""
    client_port: int = 0
    identifier: int = 0
    network_context_id: int = 0
    node_name: str = ""
    node_uuid: str = ""
    server_ip: str = ""
    sessions: list[OntapCifsConnectionSession] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
