"""OntapPerformanceIscsiMetricResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceIscsiMetricResponseIops(OntapModel):
    """OntapPerformanceIscsiMetricResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceIscsiMetricResponseLatency(OntapModel):
    """OntapPerformanceIscsiMetricResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceIscsiMetricResponseSvm(OntapModel):
    """OntapPerformanceIscsiMetricResponseSvm sub-model for svm."""

    uuid: str = ""


class OntapPerformanceIscsiMetricResponseThroughput(OntapModel):
    """OntapPerformanceIscsiMetricResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceIscsiMetricResponse(OntapModel):
    """OntapPerformanceIscsiMetricResponse information."""

    duration: str = ""
    iops: OntapPerformanceIscsiMetricResponseIops = Field(
        default_factory=OntapPerformanceIscsiMetricResponseIops
    )
    latency: OntapPerformanceIscsiMetricResponseLatency = Field(
        default_factory=OntapPerformanceIscsiMetricResponseLatency
    )
    status: str = ""
    svm: OntapPerformanceIscsiMetricResponseSvm = Field(
        default_factory=OntapPerformanceIscsiMetricResponseSvm
    )
    throughput: OntapPerformanceIscsiMetricResponseThroughput = Field(
        default_factory=OntapPerformanceIscsiMetricResponseThroughput
    )
    timestamp: str = ""
