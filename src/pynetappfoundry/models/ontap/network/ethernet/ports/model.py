"""OntapPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortDiscoveredDevice(OntapModel):
    """OntapPortDiscoveredDevice sub-model for discovered_devices."""

    capabilities: list[str] = Field(default_factory=list)
    chassis_id: str = ""
    ip_addresses: list[str] = Field(default_factory=list)
    name: str = ""
    platform: str = ""
    protocol: str = ""
    remaining_hold_time: int = 0
    remote_port: str = ""
    system_name: str = ""
    version: str = ""


class OntapPortActivePort(OntapModel):
    """OntapPortActivePort sub-model for active_ports."""

    name: str = ""
    node_name: str = ""
    uuid: str = ""


class OntapPortMemberPort(OntapModel):
    """OntapPortMemberPort sub-model for member_ports."""

    name: str = ""
    node_name: str = ""
    uuid: str = ""


class OntapPortReachableBroadcastDomain(OntapModel):
    """OntapPortReachableBroadcastDomain sub-model for reachable_broadcast_domains."""

    ipspace_name: str = ""
    name: str = ""
    uuid: str = ""


class OntapPort(OntapModel):
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
