"""OntapClusterPeer information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterPeerInitialAllowedSvm(OntapModel):
    """OntapClusterPeerInitialAllowedSvm sub-model for initial_allowed_svms."""

    initial_allowed_svms_name: str = ""
    initial_allowed_svms_uuid: str = ""


class OntapClusterPeer(OntapModel):
    """OntapClusterPeer information."""

    authentication_expiry_time: str = ""
    authentication_generate_passphrase: bool = False
    authentication_in_use: str = ""
    authentication_passphrase: str = ""
    authentication_state: str = ""
    encryption_proposed: str = ""
    encryption_state: str = ""
    initial_allowed_svms: list[OntapClusterPeerInitialAllowedSvm] = Field(default_factory=list)
    ip_address: str = ""
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    local_network_broadcast_domain: str = ""
    local_network_gateway: str = ""
    local_network_interfaces: list[dict[str, Any]] = Field(default_factory=list)
    local_network_netmask: str = ""
    name: str = ""
    peer_applications: list[str] = Field(default_factory=list)
    remote_ip_addresses: list[str] = Field(default_factory=list)
    remote_name: str = ""
    remote_serial_number: str = ""
    status_state: str = ""
    status_update_time: str = ""
    uuid: str = ""
    version_full: str = ""
    version_generation: int = 0
    version_major: int = 0
    version_minor: int = 0
