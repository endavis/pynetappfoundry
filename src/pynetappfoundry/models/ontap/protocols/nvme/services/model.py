"""OntapNvmeService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeServiceMetricFcIops(OntapModel):
    """OntapNvmeServiceMetricFcIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricFcLatency(OntapModel):
    """OntapNvmeServiceMetricFcLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricFcThroughput(OntapModel):
    """OntapNvmeServiceMetricFcThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricFc(OntapModel):
    """OntapNvmeServiceMetricFc sub-model for fc."""

    duration: str = ""
    iops: OntapNvmeServiceMetricFcIops = Field(default_factory=OntapNvmeServiceMetricFcIops)
    latency: OntapNvmeServiceMetricFcLatency = Field(
        default_factory=OntapNvmeServiceMetricFcLatency
    )
    status: str = ""
    throughput: OntapNvmeServiceMetricFcThroughput = Field(
        default_factory=OntapNvmeServiceMetricFcThroughput
    )
    timestamp: str = ""


class OntapNvmeServiceMetricIops(OntapModel):
    """OntapNvmeServiceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricLatency(OntapModel):
    """OntapNvmeServiceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricTcpIops(OntapModel):
    """OntapNvmeServiceMetricTcpIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricTcpLatency(OntapModel):
    """OntapNvmeServiceMetricTcpLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricTcpThroughput(OntapModel):
    """OntapNvmeServiceMetricTcpThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetricTcp(OntapModel):
    """OntapNvmeServiceMetricTcp sub-model for tcp."""

    duration: str = ""
    iops: OntapNvmeServiceMetricTcpIops = Field(default_factory=OntapNvmeServiceMetricTcpIops)
    latency: OntapNvmeServiceMetricTcpLatency = Field(
        default_factory=OntapNvmeServiceMetricTcpLatency
    )
    status: str = ""
    throughput: OntapNvmeServiceMetricTcpThroughput = Field(
        default_factory=OntapNvmeServiceMetricTcpThroughput
    )
    timestamp: str = ""


class OntapNvmeServiceMetricThroughput(OntapModel):
    """OntapNvmeServiceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceMetric(OntapModel):
    """OntapNvmeServiceMetric sub-model for metric."""

    duration: str = ""
    fc: OntapNvmeServiceMetricFc = Field(default_factory=OntapNvmeServiceMetricFc)
    iops: OntapNvmeServiceMetricIops = Field(default_factory=OntapNvmeServiceMetricIops)
    latency: OntapNvmeServiceMetricLatency = Field(default_factory=OntapNvmeServiceMetricLatency)
    status: str = ""
    tcp: OntapNvmeServiceMetricTcp = Field(default_factory=OntapNvmeServiceMetricTcp)
    throughput: OntapNvmeServiceMetricThroughput = Field(
        default_factory=OntapNvmeServiceMetricThroughput
    )
    timestamp: str = ""


class OntapNvmeServiceStatisticsFcIopsRaw(OntapModel):
    """OntapNvmeServiceStatisticsFcIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsFcLatencyRaw(OntapModel):
    """OntapNvmeServiceStatisticsFcLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsFcThroughputRaw(OntapModel):
    """OntapNvmeServiceStatisticsFcThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsFc(OntapModel):
    """OntapNvmeServiceStatisticsFc sub-model for fc."""

    iops_raw: OntapNvmeServiceStatisticsFcIopsRaw = Field(
        default_factory=OntapNvmeServiceStatisticsFcIopsRaw
    )
    latency_raw: OntapNvmeServiceStatisticsFcLatencyRaw = Field(
        default_factory=OntapNvmeServiceStatisticsFcLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapNvmeServiceStatisticsFcThroughputRaw = Field(
        default_factory=OntapNvmeServiceStatisticsFcThroughputRaw
    )
    timestamp: str = ""


class OntapNvmeServiceStatisticsIopsRaw(OntapModel):
    """OntapNvmeServiceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsLatencyRaw(OntapModel):
    """OntapNvmeServiceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsTcpIopsRaw(OntapModel):
    """OntapNvmeServiceStatisticsTcpIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsTcpLatencyRaw(OntapModel):
    """OntapNvmeServiceStatisticsTcpLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsTcpThroughputRaw(OntapModel):
    """OntapNvmeServiceStatisticsTcpThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatisticsTcp(OntapModel):
    """OntapNvmeServiceStatisticsTcp sub-model for tcp."""

    iops_raw: OntapNvmeServiceStatisticsTcpIopsRaw = Field(
        default_factory=OntapNvmeServiceStatisticsTcpIopsRaw
    )
    latency_raw: OntapNvmeServiceStatisticsTcpLatencyRaw = Field(
        default_factory=OntapNvmeServiceStatisticsTcpLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapNvmeServiceStatisticsTcpThroughputRaw = Field(
        default_factory=OntapNvmeServiceStatisticsTcpThroughputRaw
    )
    timestamp: str = ""


class OntapNvmeServiceStatisticsThroughputRaw(OntapModel):
    """OntapNvmeServiceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapNvmeServiceStatistics(OntapModel):
    """OntapNvmeServiceStatistics sub-model for statistics."""

    fc: OntapNvmeServiceStatisticsFc = Field(default_factory=OntapNvmeServiceStatisticsFc)
    iops_raw: OntapNvmeServiceStatisticsIopsRaw = Field(
        default_factory=OntapNvmeServiceStatisticsIopsRaw
    )
    latency_raw: OntapNvmeServiceStatisticsLatencyRaw = Field(
        default_factory=OntapNvmeServiceStatisticsLatencyRaw
    )
    status: str = ""
    tcp: OntapNvmeServiceStatisticsTcp = Field(default_factory=OntapNvmeServiceStatisticsTcp)
    throughput_raw: OntapNvmeServiceStatisticsThroughputRaw = Field(
        default_factory=OntapNvmeServiceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapNvmeServiceSvm(OntapModel):
    """OntapNvmeServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNvmeService(OntapModel):
    """OntapNvmeService information."""

    enabled: bool = False
    metric: OntapNvmeServiceMetric = Field(default_factory=OntapNvmeServiceMetric)
    statistics: OntapNvmeServiceStatistics = Field(default_factory=OntapNvmeServiceStatistics)
    svm: OntapNvmeServiceSvm = Field(default_factory=OntapNvmeServiceSvm)
