"""Network LIF information — /network/ip/interfaces."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class NetworkLIF(CacheModel):
    """Network logical interface information."""

    uuid: str = ""
    name: str = ""
    ip_address: str = ""
    netmask: str = ""
    ip_family: str = ""
    enabled: bool = True
    state: str = ""
    scope: str = ""
    vip: bool = False
    svm_uuid: str = ""
    ipspace_uuid: str = ""
    service_policy_uuid: str = ""
    services: list[str] = Field(default_factory=list)
    auto_revert: bool = False
    failover: str = ""
    is_home: bool = True
    home_node_uuid: str = ""
    home_port_uuid: str = ""
    current_node_uuid: str = ""
    current_port_uuid: str = ""
    dns_zone: str = ""
    ddns_enabled: bool = False
    subnet_uuid: str = ""
    probe_port: int = 0
    rdma_protocols: list[str] = Field(default_factory=list)
