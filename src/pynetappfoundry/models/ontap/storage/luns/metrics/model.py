"""OntapPerformanceLunMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceLunMetricResponseIops(OntapModel):
    """OntapPerformanceLunMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceLunMetricResponseLatency(OntapModel):
    """OntapPerformanceLunMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceLunMetricResponseThroughput(OntapModel):
    """OntapPerformanceLunMetricResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceLunMetricResponse(OntapModel):
    """OntapPerformanceLunMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceLunMetricResponseIops = Field(
        default_factory=OntapPerformanceLunMetricResponseIops
    )
    latency: OntapPerformanceLunMetricResponseLatency = Field(
        default_factory=OntapPerformanceLunMetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceLunMetricResponseThroughput = Field(
        default_factory=OntapPerformanceLunMetricResponseThroughput
    )
    timestamp: str = ""
    uuid: str = ""
