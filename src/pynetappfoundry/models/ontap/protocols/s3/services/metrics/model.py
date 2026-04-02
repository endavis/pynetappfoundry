"""OntapPerformanceS3MetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceS3MetricResponseIops(OntapModel):
    """OntapPerformanceS3MetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceS3MetricResponseLatency(OntapModel):
    """OntapPerformanceS3MetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceS3MetricResponseThroughput(OntapModel):
    """OntapPerformanceS3MetricResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceS3MetricResponse(OntapModel):
    """OntapPerformanceS3MetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceS3MetricResponseIops = Field(
        default_factory=OntapPerformanceS3MetricResponseIops
    )
    latency: OntapPerformanceS3MetricResponseLatency = Field(
        default_factory=OntapPerformanceS3MetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceS3MetricResponseThroughput = Field(
        default_factory=OntapPerformanceS3MetricResponseThroughput
    )
    timestamp: str = ""
