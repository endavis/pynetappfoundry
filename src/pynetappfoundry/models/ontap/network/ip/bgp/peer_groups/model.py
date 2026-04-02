"""OntapBgpPeerGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapBgpPeerGroupIpspace(OntapModel):
    """OntapBgpPeerGroupIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapBgpPeerGroupLocalInterfaceIp(OntapModel):
    """OntapBgpPeerGroupLocalInterfaceIp sub-model for ip."""

    address: str = ""


class OntapBgpPeerGroupLocalInterface(OntapModel):
    """OntapBgpPeerGroupLocalInterface sub-model for interface."""

    ip: OntapBgpPeerGroupLocalInterfaceIp = Field(default_factory=OntapBgpPeerGroupLocalInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapBgpPeerGroupLocalIp(OntapModel):
    """OntapBgpPeerGroupLocalIp sub-model for ip."""

    address: str = ""
    netmask: str = ""


class OntapBgpPeerGroupLocalPortNode(OntapModel):
    """OntapBgpPeerGroupLocalPortNode sub-model for node."""

    name: str = ""


class OntapBgpPeerGroupLocalPort(OntapModel):
    """OntapBgpPeerGroupLocalPort sub-model for port."""

    name: str = ""
    node: OntapBgpPeerGroupLocalPortNode = Field(default_factory=OntapBgpPeerGroupLocalPortNode)
    uuid: str = ""


class OntapBgpPeerGroupLocal(OntapModel):
    """OntapBgpPeerGroupLocal sub-model for local."""

    interface: OntapBgpPeerGroupLocalInterface = Field(
        default_factory=OntapBgpPeerGroupLocalInterface
    )
    ip: OntapBgpPeerGroupLocalIp = Field(default_factory=OntapBgpPeerGroupLocalIp)
    port: OntapBgpPeerGroupLocalPort = Field(default_factory=OntapBgpPeerGroupLocalPort)


class OntapBgpPeerGroupPeer(OntapModel):
    """OntapBgpPeerGroupPeer sub-model for peer."""

    address: str = ""
    asn: int = 0
    is_next_hop: bool = False
    md5_enabled: bool = False
    md5_secret: str = ""


class OntapBgpPeerGroup(OntapModel):
    """OntapBgpPeerGroup information."""

    ipspace: OntapBgpPeerGroupIpspace = Field(default_factory=OntapBgpPeerGroupIpspace)
    local: OntapBgpPeerGroupLocal = Field(default_factory=OntapBgpPeerGroupLocal)
    name: str = ""
    peer: OntapBgpPeerGroupPeer = Field(default_factory=OntapBgpPeerGroupPeer)
    state: str = ""
    uuid: str = ""
