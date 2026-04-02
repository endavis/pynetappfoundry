"""OntapTopMetricsFile information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsFileIopsError(OntapModel):
    """OntapTopMetricsFileIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsFileIops(OntapModel):
    """OntapTopMetricsFileIops sub-model for iops."""

    error: OntapTopMetricsFileIopsError = Field(default_factory=OntapTopMetricsFileIopsError)
    read: int = 0
    write: int = 0


class OntapTopMetricsFileSvm(OntapModel):
    """OntapTopMetricsFileSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsFileThroughputError(OntapModel):
    """OntapTopMetricsFileThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsFileThroughput(OntapModel):
    """OntapTopMetricsFileThroughput sub-model for throughput."""

    error: OntapTopMetricsFileThroughputError = Field(
        default_factory=OntapTopMetricsFileThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsFileVolume(OntapModel):
    """OntapTopMetricsFileVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsFile(OntapModel):
    """OntapTopMetricsFile information."""

    iops: OntapTopMetricsFileIops = Field(default_factory=OntapTopMetricsFileIops)
    path: str = ""
    svm: OntapTopMetricsFileSvm = Field(default_factory=OntapTopMetricsFileSvm)
    throughput: OntapTopMetricsFileThroughput = Field(default_factory=OntapTopMetricsFileThroughput)
    volume: OntapTopMetricsFileVolume = Field(default_factory=OntapTopMetricsFileVolume)
