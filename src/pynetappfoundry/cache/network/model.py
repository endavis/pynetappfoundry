"""Network configuration container — aggregates all network-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.name_services.dns.model import DNSInfo
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import (
    BroadcastDomain,
)
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF
from pynetappfoundry.cache.network.ip.subnets.model import IPSubnetInfo


class NetworkInfo(CacheModel):
    """Network configuration information.

    Contains LIFs, broadcast domains, IPspaces, DNS, and subnets.
    """

    intercluster_lifs: list[NetworkLIF] = Field(default_factory=list)
    data_lifs: list[NetworkLIF] = Field(default_factory=list)
    management_lifs: list[NetworkLIF] = Field(default_factory=list)
    broadcast_domains: list[BroadcastDomain] = Field(default_factory=list)
    ipspaces: list[str] = Field(default_factory=list)
    dns: list[DNSInfo] = Field(default_factory=list)
    subnets: list[IPSubnetInfo] = Field(default_factory=list)
