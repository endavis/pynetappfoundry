"""Network configuration container — aggregates all network-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel
from pynetappfoundry.models.ontap.name_services.dns.model import OntapDns
from pynetappfoundry.models.ontap.network.ethernet.broadcast_domains.model import (
    OntapBroadcastDomain,
)
from pynetappfoundry.models.ontap.network.ip.interfaces.model import OntapIpInterface
from pynetappfoundry.models.ontap.network.ip.subnets.model import OntapIpSubnet

_UNMAPPED_REASON = "Aggregate container model — not an ONTAP REST endpoint"


class NetworkInfo(OntapModel):
    """Network configuration information.

    Contains IP interfaces, ethernet broadcast domains, IPspaces, DNS,
    and IP subnets.
    """

    ip_interfaces: list[OntapIpInterface] = Field(default_factory=list)
    ethernet_broadcast_domains: list[OntapBroadcastDomain] = Field(default_factory=list)
    ipspaces: list[str] = Field(default_factory=list)
    dns: list[OntapDns] = Field(default_factory=list)
    ip_subnets: list[OntapIpSubnet] = Field(default_factory=list)
