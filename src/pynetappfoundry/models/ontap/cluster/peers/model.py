"""OntapClusterPeer information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterPeerAuthentication(OntapModel):
    """OntapClusterPeerAuthentication sub-model for authentication."""

    expiry_time: str = ""
    generate_passphrase: bool = False
    in_use: str = ""
    passphrase: str = ""
    state: str = ""


class OntapClusterPeerEncryption(OntapModel):
    """OntapClusterPeerEncryption sub-model for encryption."""

    proposed: str = ""
    state: str = ""


class OntapClusterPeerInitialAllowedSvm(OntapModel):
    """OntapClusterPeerInitialAllowedSvm sub-model for initial_allowed_svms."""

    name: str = ""
    uuid: str = ""


class OntapClusterPeerIpspace(OntapModel):
    """OntapClusterPeerIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapClusterPeerLocalNetwork(OntapModel):
    """OntapClusterPeerLocalNetwork sub-model for local_network."""

    broadcast_domain: str = ""
    gateway: str = ""
    interfaces: list[dict[str, Any]] = Field(default_factory=list)
    netmask: str = ""


class OntapClusterPeerRemote(OntapModel):
    """OntapClusterPeerRemote sub-model for remote."""

    ip_addresses: list[str] = Field(default_factory=list)
    name: str = ""
    serial_number: str = ""


class OntapClusterPeerStatus(OntapModel):
    """OntapClusterPeerStatus sub-model for status."""

    state: str = ""
    update_time: str = ""


class OntapClusterPeerVersion(OntapModel):
    """OntapClusterPeerVersion sub-model for version."""

    full: str = ""
    generation: int = 0
    major: int = 0
    minor: int = 0


class OntapClusterPeer(OntapModel):
    """OntapClusterPeer information."""

    authentication: OntapClusterPeerAuthentication = Field(
        default_factory=OntapClusterPeerAuthentication
    )
    encryption: OntapClusterPeerEncryption = Field(default_factory=OntapClusterPeerEncryption)
    initial_allowed_svms: list[OntapClusterPeerInitialAllowedSvm] = Field(default_factory=list)
    ip_address: str = ""
    ipspace: OntapClusterPeerIpspace = Field(default_factory=OntapClusterPeerIpspace)
    local_network: OntapClusterPeerLocalNetwork = Field(
        default_factory=OntapClusterPeerLocalNetwork
    )
    name: str = ""
    peer_applications: list[str] = Field(default_factory=list)
    remote: OntapClusterPeerRemote = Field(default_factory=OntapClusterPeerRemote)
    status: OntapClusterPeerStatus = Field(default_factory=OntapClusterPeerStatus)
    uuid: str = ""
    version: OntapClusterPeerVersion = Field(default_factory=OntapClusterPeerVersion)
