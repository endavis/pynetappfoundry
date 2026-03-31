"""OntapBroadcastDomain information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapBroadcastDomainPort(OntapModel):
    """OntapBroadcastDomainPort sub-model for ports."""

    name: str = ""
    node_name: str = ""
    uuid: str = ""


class OntapBroadcastDomain(OntapModel):
    """OntapBroadcastDomain information."""

    ipspace_name: str = ""
    ipspace_uuid: str = ""
    mtu: int = 0
    name: str = ""
    ports: list[OntapBroadcastDomainPort] = Field(default_factory=list)
    uuid: str = ""
