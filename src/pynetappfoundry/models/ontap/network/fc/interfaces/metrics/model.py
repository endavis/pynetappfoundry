"""OntapPerformanceFcInterfaceMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceFcInterfaceMetricResponseIops(OntapModel):
    """OntapPerformanceFcInterfaceMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcInterfaceMetricResponseLatency(OntapModel):
    """OntapPerformanceFcInterfaceMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcInterfaceMetricResponseThroughput(OntapModel):
    """OntapPerformanceFcInterfaceMetricResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceFcInterfaceMetricResponse(OntapModel):
    """OntapPerformanceFcInterfaceMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceFcInterfaceMetricResponseIops = Field(
        default_factory=OntapPerformanceFcInterfaceMetricResponseIops
    )
    latency: OntapPerformanceFcInterfaceMetricResponseLatency = Field(
        default_factory=OntapPerformanceFcInterfaceMetricResponseLatency
    )
    status: str = ""
    throughput: OntapPerformanceFcInterfaceMetricResponseThroughput = Field(
        default_factory=OntapPerformanceFcInterfaceMetricResponseThroughput
    )
    timestamp: str = ""
    uuid: str = ""
