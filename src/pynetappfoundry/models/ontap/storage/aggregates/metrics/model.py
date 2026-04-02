"""OntapPerformanceMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceMetricResponseIops(OntapModel):
    """OntapPerformanceMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceMetricResponseLatency(OntapModel):
    """OntapPerformanceMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceMetricResponseThroughput(OntapModel):
    """OntapPerformanceMetricResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceMetricResponse(OntapModel):
    """OntapPerformanceMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceMetricResponseIops = Field(
        default_factory=OntapPerformanceMetricResponseIops
    )
    latency: OntapPerformanceMetricResponseLatency = Field(
        default_factory=OntapPerformanceMetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceMetricResponseThroughput = Field(
        default_factory=OntapPerformanceMetricResponseThroughput
    )
    timestamp: str = ""
