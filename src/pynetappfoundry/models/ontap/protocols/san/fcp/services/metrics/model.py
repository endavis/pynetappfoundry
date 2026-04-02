"""OntapPerformanceFcpMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceFcpMetricResponseIops(OntapModel):
    """OntapPerformanceFcpMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcpMetricResponseLatency(OntapModel):
    """OntapPerformanceFcpMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcpMetricResponseSvm(OntapModel):
    """OntapPerformanceFcpMetricResponseSvm sub-model for svm."""

    uuid: str = ""


class OntapPerformanceFcpMetricResponseThroughput(OntapModel):
    """OntapPerformanceFcpMetricResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcpMetricResponse(OntapModel):
    """OntapPerformanceFcpMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceFcpMetricResponseIops = Field(
        default_factory=OntapPerformanceFcpMetricResponseIops
    )
    latency: OntapPerformanceFcpMetricResponseLatency = Field(
        default_factory=OntapPerformanceFcpMetricResponseLatency
    )
    status: str = ""
    svm: OntapPerformanceFcpMetricResponseSvm = Field(
        default_factory=OntapPerformanceFcpMetricResponseSvm
    )
    throughput: OntapPerformanceFcpMetricResponseThroughput = Field(
        default_factory=OntapPerformanceFcpMetricResponseThroughput
    )
    timestamp: str = ""
