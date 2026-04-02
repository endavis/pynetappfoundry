"""OntapPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortBroadcastDomainIpspace(OntapModel):
    """OntapPortBroadcastDomainIpspace sub-model for ipspace."""

    name: str = ""


class OntapPortBroadcastDomain(OntapModel):
    """OntapPortBroadcastDomain sub-model for broadcast_domain."""

    ipspace: OntapPortBroadcastDomainIpspace = Field(
        default_factory=OntapPortBroadcastDomainIpspace
    )
    name: str = ""
    uuid: str = ""


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


class OntapPortLagActivePortNode(OntapModel):
    """OntapPortLagActivePortNode sub-model for node."""

    name: str = ""


class OntapPortLagActivePort(OntapModel):
    """OntapPortLagActivePort sub-model for active_ports."""

    name: str = ""
    node: OntapPortLagActivePortNode = Field(default_factory=OntapPortLagActivePortNode)
    uuid: str = ""


class OntapPortLagMemberPortNode(OntapModel):
    """OntapPortLagMemberPortNode sub-model for node."""

    name: str = ""


class OntapPortLagMemberPort(OntapModel):
    """OntapPortLagMemberPort sub-model for member_ports."""

    name: str = ""
    node: OntapPortLagMemberPortNode = Field(default_factory=OntapPortLagMemberPortNode)
    uuid: str = ""


class OntapPortLag(OntapModel):
    """OntapPortLag sub-model for lag."""

    active_ports: list[OntapPortLagActivePort] = Field(default_factory=list)
    distribution_policy: str = ""
    member_ports: list[OntapPortLagMemberPort] = Field(default_factory=list)
    mode: str = ""


class OntapPortMetricThroughput(OntapModel):
    """OntapPortMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPortMetric(OntapModel):
    """OntapPortMetric sub-model for metric."""

    duration: str = ""
    status: str = ""
    throughput: OntapPortMetricThroughput = Field(default_factory=OntapPortMetricThroughput)
    timestamp: str = ""


class OntapPortNode(OntapModel):
    """OntapPortNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapPortReachableBroadcastDomainIpspace(OntapModel):
    """OntapPortReachableBroadcastDomainIpspace sub-model for ipspace."""

    name: str = ""


class OntapPortReachableBroadcastDomain(OntapModel):
    """OntapPortReachableBroadcastDomain sub-model for reachable_broadcast_domains."""

    ipspace: OntapPortReachableBroadcastDomainIpspace = Field(
        default_factory=OntapPortReachableBroadcastDomainIpspace
    )
    name: str = ""
    uuid: str = ""


class OntapPortStatisticsDeviceReceiveRaw(OntapModel):
    """OntapPortStatisticsDeviceReceiveRaw sub-model for receive_raw."""

    discards: int = 0
    errors: int = 0
    packets: int = 0


class OntapPortStatisticsDeviceTransmitRaw(OntapModel):
    """OntapPortStatisticsDeviceTransmitRaw sub-model for transmit_raw."""

    discards: int = 0
    errors: int = 0
    packets: int = 0


class OntapPortStatisticsDevice(OntapModel):
    """OntapPortStatisticsDevice sub-model for device."""

    link_down_count_raw: int = 0
    receive_raw: OntapPortStatisticsDeviceReceiveRaw = Field(
        default_factory=OntapPortStatisticsDeviceReceiveRaw
    )
    timestamp: str = ""
    transmit_raw: OntapPortStatisticsDeviceTransmitRaw = Field(
        default_factory=OntapPortStatisticsDeviceTransmitRaw
    )


class OntapPortStatisticsThroughputRaw(OntapModel):
    """OntapPortStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPortStatistics(OntapModel):
    """OntapPortStatistics sub-model for statistics."""

    device: OntapPortStatisticsDevice = Field(default_factory=OntapPortStatisticsDevice)
    status: str = ""
    throughput_raw: OntapPortStatisticsThroughputRaw = Field(
        default_factory=OntapPortStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapPortVlanBasePortNode(OntapModel):
    """OntapPortVlanBasePortNode sub-model for node."""

    name: str = ""


class OntapPortVlanBasePort(OntapModel):
    """OntapPortVlanBasePort sub-model for base_port."""

    name: str = ""
    node: OntapPortVlanBasePortNode = Field(default_factory=OntapPortVlanBasePortNode)
    uuid: str = ""


class OntapPortVlan(OntapModel):
    """OntapPortVlan sub-model for vlan."""

    base_port: OntapPortVlanBasePort = Field(default_factory=OntapPortVlanBasePort)
    tag: int = 0


class OntapPort(OntapModel):
    """OntapPort information."""

    broadcast_domain: OntapPortBroadcastDomain = Field(default_factory=OntapPortBroadcastDomain)
    discovered_devices: list[OntapPortDiscoveredDevice] = Field(default_factory=list)
    enabled: bool = False
    flowcontrol_admin: str = ""
    interface_count: int = 0
    lag: OntapPortLag = Field(default_factory=OntapPortLag)
    mac_address: str = ""
    metric: OntapPortMetric = Field(default_factory=OntapPortMetric)
    mtu: int = 0
    name: str = ""
    node: OntapPortNode = Field(default_factory=OntapPortNode)
    pfc_queues_admin: list[int] = Field(default_factory=list)
    rdma_protocols: list[str] = Field(default_factory=list)
    reachability: str = ""
    reachable_broadcast_domains: list[OntapPortReachableBroadcastDomain] = Field(
        default_factory=list
    )
    speed: int = 0
    state: str = ""
    statistics: OntapPortStatistics = Field(default_factory=OntapPortStatistics)
    type_: str = ""
    uuid: str = ""
    vlan: OntapPortVlan = Field(default_factory=OntapPortVlan)
