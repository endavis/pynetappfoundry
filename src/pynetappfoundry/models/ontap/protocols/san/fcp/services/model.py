"""OntapFcpService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcpServiceMetricIops(OntapModel):
    """OntapFcpServiceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcpServiceMetricLatency(OntapModel):
    """OntapFcpServiceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcpServiceMetricThroughput(OntapModel):
    """OntapFcpServiceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcpServiceMetric(OntapModel):
    """OntapFcpServiceMetric sub-model for metric."""

    duration: str = ""
    iops: OntapFcpServiceMetricIops = Field(default_factory=OntapFcpServiceMetricIops)
    latency: OntapFcpServiceMetricLatency = Field(default_factory=OntapFcpServiceMetricLatency)
    status: str = ""
    throughput: OntapFcpServiceMetricThroughput = Field(
        default_factory=OntapFcpServiceMetricThroughput
    )
    timestamp: str = ""


class OntapFcpServiceStatisticsIopsRaw(OntapModel):
    """OntapFcpServiceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcpServiceStatisticsLatencyRaw(OntapModel):
    """OntapFcpServiceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcpServiceStatisticsThroughputRaw(OntapModel):
    """OntapFcpServiceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapFcpServiceStatistics(OntapModel):
    """OntapFcpServiceStatistics sub-model for statistics."""

    iops_raw: OntapFcpServiceStatisticsIopsRaw = Field(
        default_factory=OntapFcpServiceStatisticsIopsRaw
    )
    latency_raw: OntapFcpServiceStatisticsLatencyRaw = Field(
        default_factory=OntapFcpServiceStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapFcpServiceStatisticsThroughputRaw = Field(
        default_factory=OntapFcpServiceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapFcpServiceSvm(OntapModel):
    """OntapFcpServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFcpServiceTarget(OntapModel):
    """OntapFcpServiceTarget sub-model for target."""

    name: str = ""


class OntapFcpService(OntapModel):
    """OntapFcpService information."""

    enabled: bool = False
    metric: OntapFcpServiceMetric = Field(default_factory=OntapFcpServiceMetric)
    statistics: OntapFcpServiceStatistics = Field(default_factory=OntapFcpServiceStatistics)
    svm: OntapFcpServiceSvm = Field(default_factory=OntapFcpServiceSvm)
    target: OntapFcpServiceTarget = Field(default_factory=OntapFcpServiceTarget)
