"""OntapPerformanceQtreeMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceQtreeMetricResponseIops(OntapModel):
    """OntapPerformanceQtreeMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceQtreeMetricResponseLatency(OntapModel):
    """OntapPerformanceQtreeMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceQtreeMetricResponseQtree(OntapModel):
    """OntapPerformanceQtreeMetricResponseQtree sub-model for qtree."""

    id: int = 0
    name: str = ""


class OntapPerformanceQtreeMetricResponseSvm(OntapModel):
    """OntapPerformanceQtreeMetricResponseSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPerformanceQtreeMetricResponseThroughput(OntapModel):
    """OntapPerformanceQtreeMetricResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceQtreeMetricResponseVolume(OntapModel):
    """OntapPerformanceQtreeMetricResponseVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapPerformanceQtreeMetricResponse(OntapModel):
    """OntapPerformanceQtreeMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceQtreeMetricResponseIops = Field(
        default_factory=OntapPerformanceQtreeMetricResponseIops
    )
    latency: OntapPerformanceQtreeMetricResponseLatency = Field(
        default_factory=OntapPerformanceQtreeMetricResponseLatency
    )
    qtree: OntapPerformanceQtreeMetricResponseQtree = Field(
        default_factory=OntapPerformanceQtreeMetricResponseQtree
    )
    status: str = ""
    svm: OntapPerformanceQtreeMetricResponseSvm = Field(
        default_factory=OntapPerformanceQtreeMetricResponseSvm
    )
    throughput: OntapPerformanceQtreeMetricResponseThroughput = Field(
        default_factory=OntapPerformanceQtreeMetricResponseThroughput
    )
    timestamp: str = ""
    volume: OntapPerformanceQtreeMetricResponseVolume = Field(
        default_factory=OntapPerformanceQtreeMetricResponseVolume
    )
