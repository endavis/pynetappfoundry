"""OntapVolumeMetricsResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVolumeMetricsResponseIops(OntapModel):
    """OntapVolumeMetricsResponseIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricsResponseLatency(OntapModel):
    """OntapVolumeMetricsResponseLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricsResponseThroughput(OntapModel):
    """OntapVolumeMetricsResponseThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapVolumeMetricsResponse(OntapModel):
    """OntapVolumeMetricsResponse information."""

    duration: str = ""
    iops: OntapVolumeMetricsResponseIops = Field(default_factory=OntapVolumeMetricsResponseIops)
    latency: OntapVolumeMetricsResponseLatency = Field(
        default_factory=OntapVolumeMetricsResponseLatency
    )
    status: str = ""
    throughput: OntapVolumeMetricsResponseThroughput = Field(
        default_factory=OntapVolumeMetricsResponseThroughput
    )
    timestamp: str = ""
