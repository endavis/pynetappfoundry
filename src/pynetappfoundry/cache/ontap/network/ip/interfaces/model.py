"""OntapIpInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapIpInterface(CacheModel):
    """OntapIpInterface information."""

    ddns_enabled: bool = False
    dns_zone: str = ""
    enabled: bool = False
    fail_if_subnet_conflicts: bool = False
    ip_address: str = ""
    ip_family: str = ""
    ip_netmask: str = ""
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    location_auto_revert: bool = False
    location_broadcast_domain_name: str = ""
    location_broadcast_domain_uuid: str = ""
    location_failover: str = ""
    location_home_node_name: str = ""
    location_home_node_uuid: str = ""
    location_home_port_name: str = ""
    location_home_port_node_name: str = ""
    location_home_port_uuid: str = ""
    location_is_home: bool = False
    location_node_name: str = ""
    location_node_uuid: str = ""
    location_port_name: str = ""
    location_port_node_name: str = ""
    location_port_uuid: str = ""
    metric_duration: str = ""
    metric_status: str = ""
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    name: str = ""
    probe_port: int = 0
    rdma_protocols: list[str] = Field(default_factory=list)
    scope: str = ""
    service_policy_name: str = ""
    service_policy_uuid: str = ""
    services: list[str] = Field(default_factory=list)
    state: str = ""
    statistics_status: str = ""
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    subnet_name: str = ""
    subnet_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    vip: bool = False
