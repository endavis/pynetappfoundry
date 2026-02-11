"""IP subnet information — /network/ip/subnets."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class IPSubnetInfo(CacheModel):
    """IP subnet information."""

    uuid: str = ""
    name: str = ""
    ipspace: str = ""
    broadcast_domain: str = ""
    subnet: str = ""  # CIDR notation, e.g., "10.0.0.0/24"
    gateway: str = ""
    ip_ranges: list[str] = Field(default_factory=list)
