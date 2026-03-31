"""OntapIpSubnet information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpSubnetAvailableIpRange(OntapModel):
    """OntapIpSubnetAvailableIpRange sub-model for available_ip_ranges."""

    end: str = ""
    family: str = ""


class OntapIpSubnetIpRange(OntapModel):
    """OntapIpSubnetIpRange sub-model for ip_ranges."""

    end: str = ""
    family: str = ""


class OntapIpSubnet(OntapModel):
    """OntapIpSubnet information."""

    available_count: int = 0
    available_ip_ranges: list[OntapIpSubnetAvailableIpRange] = Field(default_factory=list)
    broadcast_domain_name: str = ""
    broadcast_domain_uuid: str = ""
    fail_if_lifs_conflict: bool = False
    gateway: str = ""
    ip_ranges: list[OntapIpSubnetIpRange] = Field(default_factory=list)
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    name: str = ""
    subnet_address: str = ""
    subnet_family: str = ""
    subnet_netmask: str = ""
    total_count: int = 0
    used_count: int = 0
    uuid: str = ""
