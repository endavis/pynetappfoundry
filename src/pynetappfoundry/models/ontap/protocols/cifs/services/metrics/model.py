"""OntapPerformanceCifsMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceCifsMetricResponseIops(OntapModel):
    """OntapPerformanceCifsMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceCifsMetricResponseLatency(OntapModel):
    """OntapPerformanceCifsMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceCifsMetricResponseThroughput(OntapModel):
    """OntapPerformanceCifsMetricResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceCifsMetricResponse(OntapModel):
    """OntapPerformanceCifsMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceCifsMetricResponseIops = Field(
        default_factory=OntapPerformanceCifsMetricResponseIops
    )
    latency: OntapPerformanceCifsMetricResponseLatency = Field(
        default_factory=OntapPerformanceCifsMetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceCifsMetricResponseThroughput = Field(
        default_factory=OntapPerformanceCifsMetricResponseThroughput
    )
    timestamp: str = ""
