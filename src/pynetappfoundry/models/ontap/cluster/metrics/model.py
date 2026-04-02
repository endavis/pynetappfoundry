"""OntapClusterMetricsResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterMetricsResponseIops(OntapModel):
    """OntapClusterMetricsResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapClusterMetricsResponseLatency(OntapModel):
    """OntapClusterMetricsResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapClusterMetricsResponseThroughput(OntapModel):
    """OntapClusterMetricsResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapClusterMetricsResponse(OntapModel):
    """OntapClusterMetricsResponse information."""

    duration: str = ""
    iops: OntapClusterMetricsResponseIops = Field(default_factory=OntapClusterMetricsResponseIops)
    latency: OntapClusterMetricsResponseLatency = Field(
        default_factory=OntapClusterMetricsResponseLatency
    )
    status: str = ""
    throughput: OntapClusterMetricsResponseThroughput = Field(
        default_factory=OntapClusterMetricsResponseThroughput
    )
    timestamp: str = ""
