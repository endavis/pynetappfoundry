"""OntapIscsiService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIscsiServiceMetricIops(OntapModel):
    """OntapIscsiServiceMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapIscsiServiceMetricLatency(OntapModel):
    """OntapIscsiServiceMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapIscsiServiceMetricThroughput(OntapModel):
    """OntapIscsiServiceMetricThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapIscsiServiceMetric(OntapModel):
    """OntapIscsiServiceMetric sub-model for metric."""

    duration: str = ""
    iops: OntapIscsiServiceMetricIops = Field(default_factory=OntapIscsiServiceMetricIops)
    latency: OntapIscsiServiceMetricLatency = Field(default_factory=OntapIscsiServiceMetricLatency)
    status: str = ""
    throughput: OntapIscsiServiceMetricThroughput = Field(
        default_factory=OntapIscsiServiceMetricThroughput
    )
    timestamp: str = ""


class OntapIscsiServiceStatisticsIopsRaw(OntapModel):
    """OntapIscsiServiceStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapIscsiServiceStatisticsLatencyRaw(OntapModel):
    """OntapIscsiServiceStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapIscsiServiceStatisticsThroughputRaw(OntapModel):
    """OntapIscsiServiceStatisticsThroughputRaw sub-model for throughput_raw."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapIscsiServiceStatistics(OntapModel):
    """OntapIscsiServiceStatistics sub-model for statistics."""

    iops_raw: OntapIscsiServiceStatisticsIopsRaw = Field(
        default_factory=OntapIscsiServiceStatisticsIopsRaw
    )
    latency_raw: OntapIscsiServiceStatisticsLatencyRaw = Field(
        default_factory=OntapIscsiServiceStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapIscsiServiceStatisticsThroughputRaw = Field(
        default_factory=OntapIscsiServiceStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapIscsiServiceSvm(OntapModel):
    """OntapIscsiServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIscsiServiceTarget(OntapModel):
    """OntapIscsiServiceTarget sub-model for target."""

    alias: str = ""
    name: str = ""


class OntapIscsiService(OntapModel):
    """OntapIscsiService information."""

    enabled: bool = False
    metric: OntapIscsiServiceMetric = Field(default_factory=OntapIscsiServiceMetric)
    statistics: OntapIscsiServiceStatistics = Field(default_factory=OntapIscsiServiceStatistics)
    svm: OntapIscsiServiceSvm = Field(default_factory=OntapIscsiServiceSvm)
    target: OntapIscsiServiceTarget = Field(default_factory=OntapIscsiServiceTarget)
