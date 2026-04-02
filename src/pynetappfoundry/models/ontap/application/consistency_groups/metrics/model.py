"""OntapConsistencyGroupMetricsResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupMetricsResponseIops(OntapModel):
    """OntapConsistencyGroupMetricsResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupMetricsResponseLatency(OntapModel):
    """OntapConsistencyGroupMetricsResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupMetricsResponseThroughput(OntapModel):
    """OntapConsistencyGroupMetricsResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapConsistencyGroupMetricsResponse(OntapModel):
    """OntapConsistencyGroupMetricsResponse information."""

    available_space: int = 0
    duration: str = ""
    iops: OntapConsistencyGroupMetricsResponseIops = Field(
        default_factory=OntapConsistencyGroupMetricsResponseIops
    )
    latency: OntapConsistencyGroupMetricsResponseLatency = Field(
        default_factory=OntapConsistencyGroupMetricsResponseLatency
    )
    size: int = 0
    status: str = ""
    throughput: OntapConsistencyGroupMetricsResponseThroughput = Field(
        default_factory=OntapConsistencyGroupMetricsResponseThroughput
    )
    timestamp: str = ""
    used_space: int = 0
