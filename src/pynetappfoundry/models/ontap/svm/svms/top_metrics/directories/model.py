"""OntapTopMetricsSvmDirectory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsSvmDirectoryIopsError(OntapModel):
    """OntapTopMetricsSvmDirectoryIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmDirectoryIops(OntapModel):
    """OntapTopMetricsSvmDirectoryIops sub-model for iops."""

    error: OntapTopMetricsSvmDirectoryIopsError = Field(
        default_factory=OntapTopMetricsSvmDirectoryIopsError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmDirectorySvm(OntapModel):
    """OntapTopMetricsSvmDirectorySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmDirectoryThroughputError(OntapModel):
    """OntapTopMetricsSvmDirectoryThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmDirectoryThroughput(OntapModel):
    """OntapTopMetricsSvmDirectoryThroughput sub-model for throughput."""

    error: OntapTopMetricsSvmDirectoryThroughputError = Field(
        default_factory=OntapTopMetricsSvmDirectoryThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmDirectoryVolume(OntapModel):
    """OntapTopMetricsSvmDirectoryVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmDirectory(OntapModel):
    """OntapTopMetricsSvmDirectory information."""

    iops: OntapTopMetricsSvmDirectoryIops = Field(default_factory=OntapTopMetricsSvmDirectoryIops)
    junction_path: str = ""
    path: str = ""
    svm: OntapTopMetricsSvmDirectorySvm = Field(default_factory=OntapTopMetricsSvmDirectorySvm)
    throughput: OntapTopMetricsSvmDirectoryThroughput = Field(
        default_factory=OntapTopMetricsSvmDirectoryThroughput
    )
    volume: OntapTopMetricsSvmDirectoryVolume = Field(
        default_factory=OntapTopMetricsSvmDirectoryVolume
    )
