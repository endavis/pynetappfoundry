"""OntapBroadcastDomain information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapBroadcastDomainPort(CacheModel):
    """OntapBroadcastDomainPort sub-model for ports."""

    ports_name: str = ""
    ports_node_name: str = ""
    ports_uuid: str = ""


class OntapBroadcastDomain(CacheModel):
    """OntapBroadcastDomain information."""

    ipspace_name: str = ""
    ipspace_uuid: str = ""
    mtu: int = 0
    name: str = ""
    ports: list[OntapBroadcastDomainPort] = Field(default_factory=list)
    uuid: str = ""
