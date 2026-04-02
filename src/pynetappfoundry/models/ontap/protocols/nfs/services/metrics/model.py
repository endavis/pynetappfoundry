"""OntapPerformanceSvmNfsResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceSvmNfsResponseV3Iops(OntapModel):
    """OntapPerformanceSvmNfsResponseV3Iops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV3Latency(OntapModel):
    """OntapPerformanceSvmNfsResponseV3Latency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV3Throughput(OntapModel):
    """OntapPerformanceSvmNfsResponseV3Throughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV3(OntapModel):
    """OntapPerformanceSvmNfsResponseV3 sub-model for v3."""

    duration: str = ""
    iops: OntapPerformanceSvmNfsResponseV3Iops = Field(
        default_factory=OntapPerformanceSvmNfsResponseV3Iops
    )
    latency: OntapPerformanceSvmNfsResponseV3Latency = Field(
        default_factory=OntapPerformanceSvmNfsResponseV3Latency
    )
    status: str = ""
    throughput: OntapPerformanceSvmNfsResponseV3Throughput = Field(
        default_factory=OntapPerformanceSvmNfsResponseV3Throughput
    )
    timestamp: str = ""


class OntapPerformanceSvmNfsResponseV4Iops(OntapModel):
    """OntapPerformanceSvmNfsResponseV4Iops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV4Latency(OntapModel):
    """OntapPerformanceSvmNfsResponseV4Latency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV4Throughput(OntapModel):
    """OntapPerformanceSvmNfsResponseV4Throughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV4(OntapModel):
    """OntapPerformanceSvmNfsResponseV4 sub-model for v4."""

    duration: str = ""
    iops: OntapPerformanceSvmNfsResponseV4Iops = Field(
        default_factory=OntapPerformanceSvmNfsResponseV4Iops
    )
    latency: OntapPerformanceSvmNfsResponseV4Latency = Field(
        default_factory=OntapPerformanceSvmNfsResponseV4Latency
    )
    status: str = ""
    throughput: OntapPerformanceSvmNfsResponseV4Throughput = Field(
        default_factory=OntapPerformanceSvmNfsResponseV4Throughput
    )
    timestamp: str = ""


class OntapPerformanceSvmNfsResponseV41Iops(OntapModel):
    """OntapPerformanceSvmNfsResponseV41Iops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV41Latency(OntapModel):
    """OntapPerformanceSvmNfsResponseV41Latency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV41Throughput(OntapModel):
    """OntapPerformanceSvmNfsResponseV41Throughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPerformanceSvmNfsResponseV41(OntapModel):
    """OntapPerformanceSvmNfsResponseV41 sub-model for v41."""

    duration: str = ""
    iops: OntapPerformanceSvmNfsResponseV41Iops = Field(
        default_factory=OntapPerformanceSvmNfsResponseV41Iops
    )
    latency: OntapPerformanceSvmNfsResponseV41Latency = Field(
        default_factory=OntapPerformanceSvmNfsResponseV41Latency
    )
    status: str = ""
    throughput: OntapPerformanceSvmNfsResponseV41Throughput = Field(
        default_factory=OntapPerformanceSvmNfsResponseV41Throughput
    )
    timestamp: str = ""


class OntapPerformanceSvmNfsResponse(OntapModel):
    """OntapPerformanceSvmNfsResponse information."""

    v3: OntapPerformanceSvmNfsResponseV3 = Field(default_factory=OntapPerformanceSvmNfsResponseV3)
    v4: OntapPerformanceSvmNfsResponseV4 = Field(default_factory=OntapPerformanceSvmNfsResponseV4)
    v41: OntapPerformanceSvmNfsResponseV41 = Field(
        default_factory=OntapPerformanceSvmNfsResponseV41
    )
