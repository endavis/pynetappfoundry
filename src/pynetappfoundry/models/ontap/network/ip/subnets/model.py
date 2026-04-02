"""OntapIpSubnet information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpSubnetAvailableIpRange(OntapModel):
    """OntapIpSubnetAvailableIpRange sub-model for available_ip_ranges."""

    end: str = ""
    family: str = ""


class OntapIpSubnetBroadcastDomain(OntapModel):
    """OntapIpSubnetBroadcastDomain sub-model for broadcast_domain."""

    name: str = ""
    uuid: str = ""


class OntapIpSubnetIpRange(OntapModel):
    """OntapIpSubnetIpRange sub-model for ip_ranges."""

    end: str = ""
    family: str = ""


class OntapIpSubnetIpspace(OntapModel):
    """OntapIpSubnetIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapIpSubnetSubnet(OntapModel):
    """OntapIpSubnetSubnet sub-model for subnet."""

    address: str = ""
    family: str = ""
    netmask: str = ""


class OntapIpSubnet(OntapModel):
    """OntapIpSubnet information."""

    available_count: int = 0
    available_ip_ranges: list[OntapIpSubnetAvailableIpRange] = Field(default_factory=list)
    broadcast_domain: OntapIpSubnetBroadcastDomain = Field(
        default_factory=OntapIpSubnetBroadcastDomain
    )
    fail_if_lifs_conflict: bool = False
    gateway: str = ""
    ip_ranges: list[OntapIpSubnetIpRange] = Field(default_factory=list)
    ipspace: OntapIpSubnetIpspace = Field(default_factory=OntapIpSubnetIpspace)
    name: str = ""
    subnet: OntapIpSubnetSubnet = Field(default_factory=OntapIpSubnetSubnet)
    total_count: int = 0
    used_count: int = 0
    uuid: str = ""
