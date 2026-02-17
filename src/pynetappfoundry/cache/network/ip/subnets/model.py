"""OntapIpSubnet information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapIpSubnetAvailableIpRange(CacheModel):
    """OntapIpSubnetAvailableIpRange sub-model for available_ip_ranges."""

    available_ip_ranges_end: str = ""
    available_ip_ranges_family: str = ""


class OntapIpSubnetIpRange(CacheModel):
    """OntapIpSubnetIpRange sub-model for ip_ranges."""

    ip_ranges_end: str = ""
    ip_ranges_family: str = ""


class OntapIpSubnet(CacheModel):
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
