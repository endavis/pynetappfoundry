"""OntapFcPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcPortFabric(OntapModel):
    """OntapFcPortFabric sub-model for fabric."""

    connected: bool = False
    connected_speed: int = 0
    name: str = ""
    port_address: str = ""
    switch_port: str = ""


class OntapFcPortMetricIops(OntapModel):
    """OntapFcPortMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcPortMetricLatency(OntapModel):
    """OntapFcPortMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcPortMetricThroughput(OntapModel):
    """OntapFcPortMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcPortMetric(OntapModel):
    """OntapFcPortMetric sub-model for metric."""

    duration: str = ""
    iops: OntapFcPortMetricIops = Field(default_factory=OntapFcPortMetricIops)
    latency: OntapFcPortMetricLatency = Field(default_factory=OntapFcPortMetricLatency)
    status: str = ""
    throughput: OntapFcPortMetricThroughput = Field(default_factory=OntapFcPortMetricThroughput)
    timestamp: str = ""


class OntapFcPortNode(OntapModel):
    """OntapFcPortNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapFcPortSpeed(OntapModel):
    """OntapFcPortSpeed sub-model for speed."""

    configured: str = ""
    maximum: str = ""


class OntapFcPortStatisticsIopsRaw(OntapModel):
    """OntapFcPortStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcPortStatisticsLatencyRaw(OntapModel):
    """OntapFcPortStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcPortStatisticsThroughputRaw(OntapModel):
    """OntapFcPortStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcPortStatistics(OntapModel):
    """OntapFcPortStatistics sub-model for statistics."""

    iops_raw: OntapFcPortStatisticsIopsRaw = Field(default_factory=OntapFcPortStatisticsIopsRaw)
    latency_raw: OntapFcPortStatisticsLatencyRaw = Field(
        default_factory=OntapFcPortStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapFcPortStatisticsThroughputRaw = Field(
        default_factory=OntapFcPortStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapFcPortTransceiver(OntapModel):
    """OntapFcPortTransceiver sub-model for transceiver."""

    capabilities: list[int] = Field(default_factory=list)
    form_factor: str = ""
    manufacturer: str = ""
    part_number: str = ""


class OntapFcPort(OntapModel):
    """OntapFcPort information."""

    description: str = ""
    enabled: bool = False
    fabric: OntapFcPortFabric = Field(default_factory=OntapFcPortFabric)
    interface_count: int = 0
    metric: OntapFcPortMetric = Field(default_factory=OntapFcPortMetric)
    name: str = ""
    node: OntapFcPortNode = Field(default_factory=OntapFcPortNode)
    physical_protocol: str = ""
    speed: OntapFcPortSpeed = Field(default_factory=OntapFcPortSpeed)
    state: str = ""
    statistics: OntapFcPortStatistics = Field(default_factory=OntapFcPortStatistics)
    supported_protocols: list[str] = Field(default_factory=list)
    transceiver: OntapFcPortTransceiver = Field(default_factory=OntapFcPortTransceiver)
    uuid: str = ""
    wwnn: str = ""
    wwpn: str = ""
