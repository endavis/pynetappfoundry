"""OntapPerformanceNamespaceMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceNamespaceMetricResponseIops(OntapModel):
    """OntapPerformanceNamespaceMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNamespaceMetricResponseLatency(OntapModel):
    """OntapPerformanceNamespaceMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNamespaceMetricResponseThroughput(OntapModel):
    """OntapPerformanceNamespaceMetricResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceNamespaceMetricResponse(OntapModel):
    """OntapPerformanceNamespaceMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceNamespaceMetricResponseIops = Field(
        default_factory=OntapPerformanceNamespaceMetricResponseIops
    )
    latency: OntapPerformanceNamespaceMetricResponseLatency = Field(
        default_factory=OntapPerformanceNamespaceMetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceNamespaceMetricResponseThroughput = Field(
        default_factory=OntapPerformanceNamespaceMetricResponseThroughput
    )
    timestamp: str = ""
    uuid: str = ""
