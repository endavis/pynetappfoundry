"""OntapTopMetricsDirectory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsDirectoryIopsError(OntapModel):
    """OntapTopMetricsDirectoryIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsDirectoryIops(OntapModel):
    """OntapTopMetricsDirectoryIops sub-model for iops."""

    error: OntapTopMetricsDirectoryIopsError = Field(
        default_factory=OntapTopMetricsDirectoryIopsError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsDirectorySvm(OntapModel):
    """OntapTopMetricsDirectorySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsDirectoryThroughputError(OntapModel):
    """OntapTopMetricsDirectoryThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsDirectoryThroughput(OntapModel):
    """OntapTopMetricsDirectoryThroughput sub-model for throughput."""

    error: OntapTopMetricsDirectoryThroughputError = Field(
        default_factory=OntapTopMetricsDirectoryThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsDirectoryVolume(OntapModel):
    """OntapTopMetricsDirectoryVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsDirectory(OntapModel):
    """OntapTopMetricsDirectory information."""

    iops: OntapTopMetricsDirectoryIops = Field(default_factory=OntapTopMetricsDirectoryIops)
    non_recursive_bytes_used: int = 0
    path: str = ""
    svm: OntapTopMetricsDirectorySvm = Field(default_factory=OntapTopMetricsDirectorySvm)
    throughput: OntapTopMetricsDirectoryThroughput = Field(
        default_factory=OntapTopMetricsDirectoryThroughput
    )
    volume: OntapTopMetricsDirectoryVolume = Field(default_factory=OntapTopMetricsDirectoryVolume)
