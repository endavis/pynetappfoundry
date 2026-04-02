"""OntapCifsSession information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsSessionNode(OntapModel):
    """OntapCifsSessionNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCifsSessionSvm(OntapModel):
    """OntapCifsSessionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsSessionVolume(OntapModel):
    """OntapCifsSessionVolume sub-model for volumes."""

    name: str = ""
    uuid: str = ""


class OntapCifsSession(OntapModel):
    """OntapCifsSession information."""

    authentication: str = ""
    client_ip: str = ""
    connected_duration: str = ""
    connection_count: int = 0
    connection_id: int = 0
    continuous_availability: str = ""
    identifier: int = 0
    idle_duration: str = ""
    large_mtu: bool = False
    mapped_unix_user: str = ""
    node: OntapCifsSessionNode = Field(default_factory=OntapCifsSessionNode)
    open_files: int = 0
    open_other: int = 0
    open_shares: int = 0
    protocol: str = ""
    server_ip: str = ""
    smb_encryption: str = ""
    smb_signing: bool = False
    svm: OntapCifsSessionSvm = Field(default_factory=OntapCifsSessionSvm)
    user: str = ""
    volumes: list[OntapCifsSessionVolume] = Field(default_factory=list)
