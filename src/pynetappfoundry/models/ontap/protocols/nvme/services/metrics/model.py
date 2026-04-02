"""OntapPerformanceNvmeMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceNvmeMetricResponseFcIops(OntapModel):
    """OntapPerformanceNvmeMetricResponseFcIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseFcLatency(OntapModel):
    """OntapPerformanceNvmeMetricResponseFcLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseFcThroughput(OntapModel):
    """OntapPerformanceNvmeMetricResponseFcThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseFc(OntapModel):
    """OntapPerformanceNvmeMetricResponseFc sub-model for fc."""

    duration: str = ""
    iops: OntapPerformanceNvmeMetricResponseFcIops = Field(
        default_factory=OntapPerformanceNvmeMetricResponseFcIops
    )
    latency: OntapPerformanceNvmeMetricResponseFcLatency = Field(
        default_factory=OntapPerformanceNvmeMetricResponseFcLatency
    )
    status: str = ""
    throughput: OntapPerformanceNvmeMetricResponseFcThroughput = Field(
        default_factory=OntapPerformanceNvmeMetricResponseFcThroughput
    )


class OntapPerformanceNvmeMetricResponseIops(OntapModel):
    """OntapPerformanceNvmeMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseLatency(OntapModel):
    """OntapPerformanceNvmeMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseSvm(OntapModel):
    """OntapPerformanceNvmeMetricResponseSvm sub-model for svm."""

    uuid: str = ""


class OntapPerformanceNvmeMetricResponseTcpIops(OntapModel):
    """OntapPerformanceNvmeMetricResponseTcpIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseTcpLatency(OntapModel):
    """OntapPerformanceNvmeMetricResponseTcpLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseTcpThroughput(OntapModel):
    """OntapPerformanceNvmeMetricResponseTcpThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponseTcp(OntapModel):
    """OntapPerformanceNvmeMetricResponseTcp sub-model for tcp."""

    duration: str = ""
    iops: OntapPerformanceNvmeMetricResponseTcpIops = Field(
        default_factory=OntapPerformanceNvmeMetricResponseTcpIops
    )
    latency: OntapPerformanceNvmeMetricResponseTcpLatency = Field(
        default_factory=OntapPerformanceNvmeMetricResponseTcpLatency
    )
    status: str = ""
    throughput: OntapPerformanceNvmeMetricResponseTcpThroughput = Field(
        default_factory=OntapPerformanceNvmeMetricResponseTcpThroughput
    )


class OntapPerformanceNvmeMetricResponseThroughput(OntapModel):
    """OntapPerformanceNvmeMetricResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNvmeMetricResponse(OntapModel):
    """OntapPerformanceNvmeMetricResponse information."""

    duration: str = ""
    fc: OntapPerformanceNvmeMetricResponseFc = Field(
        default_factory=OntapPerformanceNvmeMetricResponseFc
    )
    iops: OntapPerformanceNvmeMetricResponseIops = Field(
        default_factory=OntapPerformanceNvmeMetricResponseIops
    )
    latency: OntapPerformanceNvmeMetricResponseLatency = Field(
        default_factory=OntapPerformanceNvmeMetricResponseLatency
    )
    status: str = ""
    svm: OntapPerformanceNvmeMetricResponseSvm = Field(
        default_factory=OntapPerformanceNvmeMetricResponseSvm
    )
    tcp: OntapPerformanceNvmeMetricResponseTcp = Field(
        default_factory=OntapPerformanceNvmeMetricResponseTcp
    )
    throughput: OntapPerformanceNvmeMetricResponseThroughput = Field(
        default_factory=OntapPerformanceNvmeMetricResponseThroughput
    )
    timestamp: str = ""
