"""OntapBroadcastDomain information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapBroadcastDomainIpspace(OntapModel):
    """OntapBroadcastDomainIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapBroadcastDomainPortNode(OntapModel):
    """OntapBroadcastDomainPortNode sub-model for node."""

    name: str = ""


class OntapBroadcastDomainPort(OntapModel):
    """OntapBroadcastDomainPort sub-model for ports."""

    name: str = ""
    node: OntapBroadcastDomainPortNode = Field(default_factory=OntapBroadcastDomainPortNode)
    uuid: str = ""


class OntapBroadcastDomain(OntapModel):
    """OntapBroadcastDomain information."""

    ipspace: OntapBroadcastDomainIpspace = Field(default_factory=OntapBroadcastDomainIpspace)
    mtu: int = 0
    name: str = ""
    ports: list[OntapBroadcastDomainPort] = Field(default_factory=list)
    uuid: str = ""
