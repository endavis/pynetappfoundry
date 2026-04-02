"""OntapFcInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcInterfaceLocationHomeNode(OntapModel):
    """OntapFcInterfaceLocationHomeNode sub-model for home_node."""

    name: str = ""
    uuid: str = ""


class OntapFcInterfaceLocationHomePortNode(OntapModel):
    """OntapFcInterfaceLocationHomePortNode sub-model for node."""

    name: str = ""


class OntapFcInterfaceLocationHomePort(OntapModel):
    """OntapFcInterfaceLocationHomePort sub-model for home_port."""

    name: str = ""
    node: OntapFcInterfaceLocationHomePortNode = Field(
        default_factory=OntapFcInterfaceLocationHomePortNode
    )
    uuid: str = ""


class OntapFcInterfaceLocationNode(OntapModel):
    """OntapFcInterfaceLocationNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapFcInterfaceLocationPortNode(OntapModel):
    """OntapFcInterfaceLocationPortNode sub-model for node."""

    name: str = ""


class OntapFcInterfaceLocationPort(OntapModel):
    """OntapFcInterfaceLocationPort sub-model for port."""

    name: str = ""
    node: OntapFcInterfaceLocationPortNode = Field(default_factory=OntapFcInterfaceLocationPortNode)
    uuid: str = ""


class OntapFcInterfaceLocation(OntapModel):
    """OntapFcInterfaceLocation sub-model for location."""

    home_node: OntapFcInterfaceLocationHomeNode = Field(
        default_factory=OntapFcInterfaceLocationHomeNode
    )
    home_port: OntapFcInterfaceLocationHomePort = Field(
        default_factory=OntapFcInterfaceLocationHomePort
    )
    is_home: bool = False
    node: OntapFcInterfaceLocationNode = Field(default_factory=OntapFcInterfaceLocationNode)
    port: OntapFcInterfaceLocationPort = Field(default_factory=OntapFcInterfaceLocationPort)


class OntapFcInterfaceMetricIops(OntapModel):
    """OntapFcInterfaceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcInterfaceMetricLatency(OntapModel):
    """OntapFcInterfaceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcInterfaceMetricThroughput(OntapModel):
    """OntapFcInterfaceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcInterfaceMetric(OntapModel):
    """OntapFcInterfaceMetric sub-model for metric."""

    duration: str = ""
    iops: OntapFcInterfaceMetricIops = Field(default_factory=OntapFcInterfaceMetricIops)
    latency: OntapFcInterfaceMetricLatency = Field(default_factory=OntapFcInterfaceMetricLatency)
    status: str = ""
    throughput: OntapFcInterfaceMetricThroughput = Field(
        default_factory=OntapFcInterfaceMetricThroughput
    )
    timestamp: str = ""


class OntapFcInterfaceStatisticsIopsRaw(OntapModel):
    """OntapFcInterfaceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcInterfaceStatisticsLatencyRaw(OntapModel):
    """OntapFcInterfaceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcInterfaceStatisticsThroughputRaw(OntapModel):
    """OntapFcInterfaceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcInterfaceStatistics(OntapModel):
    """OntapFcInterfaceStatistics sub-model for statistics."""

    iops_raw: OntapFcInterfaceStatisticsIopsRaw = Field(
        default_factory=OntapFcInterfaceStatisticsIopsRaw
    )
    latency_raw: OntapFcInterfaceStatisticsLatencyRaw = Field(
        default_factory=OntapFcInterfaceStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapFcInterfaceStatisticsThroughputRaw = Field(
        default_factory=OntapFcInterfaceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapFcInterfaceSvm(OntapModel):
    """OntapFcInterfaceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFcInterface(OntapModel):
    """OntapFcInterface information."""

    comment: str = ""
    data_protocol: str = ""
    enabled: bool = False
    location: OntapFcInterfaceLocation = Field(default_factory=OntapFcInterfaceLocation)
    metric: OntapFcInterfaceMetric = Field(default_factory=OntapFcInterfaceMetric)
    name: str = ""
    port_address: str = ""
    state: str = ""
    statistics: OntapFcInterfaceStatistics = Field(default_factory=OntapFcInterfaceStatistics)
    svm: OntapFcInterfaceSvm = Field(default_factory=OntapFcInterfaceSvm)
    uuid: str = ""
    wwnn: str = ""
    wwpn: str = ""
