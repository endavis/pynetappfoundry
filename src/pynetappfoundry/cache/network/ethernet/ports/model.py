"""OntapPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapPortDiscoveredDevice(CacheModel):
    """OntapPortDiscoveredDevice sub-model for discovered_devices."""

    discovered_devices_capabilities: list[str] = Field(default_factory=list)
    discovered_devices_chassis_id: str = ""
    discovered_devices_ip_addresses: list[str] = Field(default_factory=list)
    discovered_devices_name: str = ""
    discovered_devices_platform: str = ""
    discovered_devices_protocol: str = ""
    discovered_devices_remaining_hold_time: int = 0
    discovered_devices_remote_port: str = ""
    discovered_devices_system_name: str = ""
    discovered_devices_version: str = ""


class OntapPortActivePort(CacheModel):
    """OntapPortActivePort sub-model for active_ports."""

    lag_active_ports_name: str = ""
    lag_active_ports_node_name: str = ""
    lag_active_ports_uuid: str = ""


class OntapPortMemberPort(CacheModel):
    """OntapPortMemberPort sub-model for member_ports."""

    lag_member_ports_name: str = ""
    lag_member_ports_node_name: str = ""
    lag_member_ports_uuid: str = ""


class OntapPortReachableBroadcastDomain(CacheModel):
    """OntapPortReachableBroadcastDomain sub-model for reachable_broadcast_domains."""

    reachable_broadcast_domains_ipspace_name: str = ""
    reachable_broadcast_domains_name: str = ""
    reachable_broadcast_domains_uuid: str = ""


class OntapPort(CacheModel):
    """OntapPort information."""

    broadcast_domain_ipspace_name: str = ""
    broadcast_domain_name: str = ""
    broadcast_domain_uuid: str = ""
    discovered_devices: list[OntapPortDiscoveredDevice] = Field(default_factory=list)
    enabled: bool = False
    flowcontrol_admin: str = ""
    interface_count: int = 0
    lag_active_ports: list[OntapPortActivePort] = Field(default_factory=list)
    lag_distribution_policy: str = ""
    lag_member_ports: list[OntapPortMemberPort] = Field(default_factory=list)
    lag_mode: str = ""
    mac_address: str = ""
    metric_duration: str = ""
    metric_status: str = ""
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    mtu: int = 0
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    pfc_queues_admin: list[int] = Field(default_factory=list)
    rdma_protocols: list[str] = Field(default_factory=list)
    reachability: str = ""
    reachable_broadcast_domains: list[OntapPortReachableBroadcastDomain] = Field(
        default_factory=list
    )
    speed: int = 0
    state: str = ""
    statistics_device_link_down_count_raw: int = 0
    statistics_device_receive_raw_discards: int = 0
    statistics_device_receive_raw_errors: int = 0
    statistics_device_receive_raw_packets: int = 0
    statistics_device_timestamp: str = ""
    statistics_device_transmit_raw_discards: int = 0
    statistics_device_transmit_raw_errors: int = 0
    statistics_device_transmit_raw_packets: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    type_: str = ""
    uuid: str = ""
    vlan_base_port_name: str = ""
    vlan_base_port_node_name: str = ""
    vlan_base_port_uuid: str = ""
    vlan_tag: int = 0
