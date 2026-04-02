"""OntapPerformanceFcPortMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceFcPortMetricResponseIops(OntapModel):
    """OntapPerformanceFcPortMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcPortMetricResponseLatency(OntapModel):
    """OntapPerformanceFcPortMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcPortMetricResponseThroughput(OntapModel):
    """OntapPerformanceFcPortMetricResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcPortMetricResponse(OntapModel):
    """OntapPerformanceFcPortMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceFcPortMetricResponseIops = Field(
        default_factory=OntapPerformanceFcPortMetricResponseIops
    )
    latency: OntapPerformanceFcPortMetricResponseLatency = Field(
        default_factory=OntapPerformanceFcPortMetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceFcPortMetricResponseThroughput = Field(
        default_factory=OntapPerformanceFcPortMetricResponseThroughput
    )
    timestamp: str = ""
    uuid: str = ""
