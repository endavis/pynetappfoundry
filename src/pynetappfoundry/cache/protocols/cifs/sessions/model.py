"""OntapCifsSession information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapCifsSessionVolume(CacheModel):
    """OntapCifsSessionVolume sub-model for volumes."""

    volumes_name: str = ""
    volumes_uuid: str = ""


class OntapCifsSession(CacheModel):
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
    node_name: str = ""
    node_uuid: str = ""
    open_files: int = 0
    open_other: int = 0
    open_shares: int = 0
    protocol: str = ""
    server_ip: str = ""
    smb_encryption: str = ""
    smb_signing: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    user: str = ""
    volumes: list[OntapCifsSessionVolume] = Field(default_factory=list)
