"""Network configuration container — aggregates all network-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.ontap.name_services.dns.model import OntapDns
from pynetappfoundry.cache.ontap.network.ethernet.broadcast_domains.model import (
    OntapBroadcastDomain,
)
from pynetappfoundry.cache.ontap.network.ip.interfaces.model import OntapIpInterface
from pynetappfoundry.cache.ontap.network.ip.subnets.model import OntapIpSubnet


class NetworkInfo(CacheModel):
    """Network configuration information.

    Contains IP interfaces, ethernet broadcast domains, IPspaces, DNS,
    and IP subnets.
    """

    ip_interfaces: list[OntapIpInterface] = Field(default_factory=list)
    ethernet_broadcast_domains: list[OntapBroadcastDomain] = Field(default_factory=list)
    ipspaces: list[str] = Field(default_factory=list)
    dns: list[OntapDns] = Field(default_factory=list)
    ip_subnets: list[OntapIpSubnet] = Field(default_factory=list)
