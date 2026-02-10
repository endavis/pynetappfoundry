"""Network interface and domain models (/network API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class NetworkLIF(BaseModel):
    """Network logical interface information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    ip_address: str = ""
    netmask: str = ""
    home_node: str = ""
    home_port: str = ""
    role: str = ""  # data, cluster, intercluster, management
    svm: str = ""


class BroadcastDomain(BaseModel):
    """Broadcast domain configuration."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    ipspace: str = ""
    mtu: int = 0
    ports: list[str] = Field(default_factory=list)


class IPSubnetInfo(BaseModel):
    """IP subnet information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    ipspace: str = ""
    broadcast_domain: str = ""
    subnet: str = ""  # CIDR notation, e.g., "10.0.0.0/24"
    gateway: str = ""
    ip_ranges: list[str] = Field(default_factory=list)
