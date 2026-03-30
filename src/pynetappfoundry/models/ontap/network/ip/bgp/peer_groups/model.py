"""OntapBgpPeerGroup information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapBgpPeerGroup(OntapModel):
    """OntapBgpPeerGroup information."""

    ipspace_name: str = ""
    ipspace_uuid: str = ""
    local_interface_ip_address: str = ""
    local_interface_name: str = ""
    local_interface_uuid: str = ""
    local_ip_address: str = ""
    local_ip_netmask: str = ""
    local_port_name: str = ""
    local_port_node_name: str = ""
    local_port_uuid: str = ""
    name: str = ""
    peer_address: str = ""
    peer_asn: int = 0
    peer_is_next_hop: bool = False
    peer_md5_enabled: bool = False
    peer_md5_secret: str = ""
    state: str = ""
    uuid: str = ""
