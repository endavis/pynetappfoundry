"""OntapTopMetricsSvmFile information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsSvmFileIopsError(OntapModel):
    """OntapTopMetricsSvmFileIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmFileIops(OntapModel):
    """OntapTopMetricsSvmFileIops sub-model for iops."""

    error: OntapTopMetricsSvmFileIopsError = Field(default_factory=OntapTopMetricsSvmFileIopsError)
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmFileSvm(OntapModel):
    """OntapTopMetricsSvmFileSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmFileThroughputError(OntapModel):
    """OntapTopMetricsSvmFileThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmFileThroughput(OntapModel):
    """OntapTopMetricsSvmFileThroughput sub-model for throughput."""

    error: OntapTopMetricsSvmFileThroughputError = Field(
        default_factory=OntapTopMetricsSvmFileThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmFileVolume(OntapModel):
    """OntapTopMetricsSvmFileVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmFile(OntapModel):
    """OntapTopMetricsSvmFile information."""

    iops: OntapTopMetricsSvmFileIops = Field(default_factory=OntapTopMetricsSvmFileIops)
    junction_path: str = ""
    path: str = ""
    svm: OntapTopMetricsSvmFileSvm = Field(default_factory=OntapTopMetricsSvmFileSvm)
    throughput: OntapTopMetricsSvmFileThroughput = Field(
        default_factory=OntapTopMetricsSvmFileThroughput
    )
    volume: OntapTopMetricsSvmFileVolume = Field(default_factory=OntapTopMetricsSvmFileVolume)
