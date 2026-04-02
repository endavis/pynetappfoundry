"""OntapIpInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpInterfaceIp(OntapModel):
    """OntapIpInterfaceIp sub-model for ip."""

    address: str = ""
    family: str = ""
    netmask: str = ""


class OntapIpInterfaceIpspace(OntapModel):
    """OntapIpInterfaceIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapIpInterfaceLocationBroadcastDomain(OntapModel):
    """OntapIpInterfaceLocationBroadcastDomain sub-model for broadcast_domain."""

    name: str = ""
    uuid: str = ""


class OntapIpInterfaceLocationHomeNode(OntapModel):
    """OntapIpInterfaceLocationHomeNode sub-model for home_node."""

    name: str = ""
    uuid: str = ""


class OntapIpInterfaceLocationHomePortNode(OntapModel):
    """OntapIpInterfaceLocationHomePortNode sub-model for node."""

    name: str = ""


class OntapIpInterfaceLocationHomePort(OntapModel):
    """OntapIpInterfaceLocationHomePort sub-model for home_port."""

    name: str = ""
    node: OntapIpInterfaceLocationHomePortNode = Field(
        default_factory=OntapIpInterfaceLocationHomePortNode
    )
    uuid: str = ""


class OntapIpInterfaceLocationNode(OntapModel):
    """OntapIpInterfaceLocationNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapIpInterfaceLocationPortNode(OntapModel):
    """OntapIpInterfaceLocationPortNode sub-model for node."""

    name: str = ""


class OntapIpInterfaceLocationPort(OntapModel):
    """OntapIpInterfaceLocationPort sub-model for port."""

    name: str = ""
    node: OntapIpInterfaceLocationPortNode = Field(default_factory=OntapIpInterfaceLocationPortNode)
    uuid: str = ""


class OntapIpInterfaceLocation(OntapModel):
    """OntapIpInterfaceLocation sub-model for location."""

    auto_revert: bool = False
    broadcast_domain: OntapIpInterfaceLocationBroadcastDomain = Field(
        default_factory=OntapIpInterfaceLocationBroadcastDomain
    )
    failover: str = ""
    home_node: OntapIpInterfaceLocationHomeNode = Field(
        default_factory=OntapIpInterfaceLocationHomeNode
    )
    home_port: OntapIpInterfaceLocationHomePort = Field(
        default_factory=OntapIpInterfaceLocationHomePort
    )
    is_home: bool = False
    node: OntapIpInterfaceLocationNode = Field(default_factory=OntapIpInterfaceLocationNode)
    port: OntapIpInterfaceLocationPort = Field(default_factory=OntapIpInterfaceLocationPort)


class OntapIpInterfaceMetricThroughput(OntapModel):
    """OntapIpInterfaceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapIpInterfaceMetric(OntapModel):
    """OntapIpInterfaceMetric sub-model for metric."""

    duration: str = ""
    status: str = ""
    throughput: OntapIpInterfaceMetricThroughput = Field(
        default_factory=OntapIpInterfaceMetricThroughput
    )
    timestamp: str = ""


class OntapIpInterfaceServicePolicy(OntapModel):
    """OntapIpInterfaceServicePolicy sub-model for service_policy."""

    name: str = ""
    uuid: str = ""


class OntapIpInterfaceStatisticsThroughputRaw(OntapModel):
    """OntapIpInterfaceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapIpInterfaceStatistics(OntapModel):
    """OntapIpInterfaceStatistics sub-model for statistics."""

    status: str = ""
    throughput_raw: OntapIpInterfaceStatisticsThroughputRaw = Field(
        default_factory=OntapIpInterfaceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapIpInterfaceSubnet(OntapModel):
    """OntapIpInterfaceSubnet sub-model for subnet."""

    name: str = ""
    uuid: str = ""


class OntapIpInterfaceSvm(OntapModel):
    """OntapIpInterfaceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIpInterface(OntapModel):
    """OntapIpInterface information."""

    ddns_enabled: bool = False
    dns_zone: str = ""
    enabled: bool = False
    fail_if_subnet_conflicts: bool = False
    ip: OntapIpInterfaceIp = Field(default_factory=OntapIpInterfaceIp)
    ipspace: OntapIpInterfaceIpspace = Field(default_factory=OntapIpInterfaceIpspace)
    location: OntapIpInterfaceLocation = Field(default_factory=OntapIpInterfaceLocation)
    metric: OntapIpInterfaceMetric = Field(default_factory=OntapIpInterfaceMetric)
    name: str = ""
    probe_port: int = 0
    rdma_protocols: list[str] = Field(default_factory=list)
    scope: str = ""
    service_policy: OntapIpInterfaceServicePolicy = Field(
        default_factory=OntapIpInterfaceServicePolicy
    )
    services: list[str] = Field(default_factory=list)
    state: str = ""
    statistics: OntapIpInterfaceStatistics = Field(default_factory=OntapIpInterfaceStatistics)
    subnet: OntapIpInterfaceSubnet = Field(default_factory=OntapIpInterfaceSubnet)
    svm: OntapIpInterfaceSvm = Field(default_factory=OntapIpInterfaceSvm)
    uuid: str = ""
    vip: bool = False
