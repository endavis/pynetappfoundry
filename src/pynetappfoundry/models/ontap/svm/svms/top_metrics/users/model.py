"""OntapTopMetricsSvmUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsSvmUserIopsError(OntapModel):
    """OntapTopMetricsSvmUserIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmUserIops(OntapModel):
    """OntapTopMetricsSvmUserIops sub-model for iops."""

    error: OntapTopMetricsSvmUserIopsError = Field(default_factory=OntapTopMetricsSvmUserIopsError)
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmUserSvm(OntapModel):
    """OntapTopMetricsSvmUserSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmUserThroughputError(OntapModel):
    """OntapTopMetricsSvmUserThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmUserThroughput(OntapModel):
    """OntapTopMetricsSvmUserThroughput sub-model for throughput."""

    error: OntapTopMetricsSvmUserThroughputError = Field(
        default_factory=OntapTopMetricsSvmUserThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmUserVolume(OntapModel):
    """OntapTopMetricsSvmUserVolume sub-model for volumes."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmUser(OntapModel):
    """OntapTopMetricsSvmUser information."""

    iops: OntapTopMetricsSvmUserIops = Field(default_factory=OntapTopMetricsSvmUserIops)
    svm: OntapTopMetricsSvmUserSvm = Field(default_factory=OntapTopMetricsSvmUserSvm)
    throughput: OntapTopMetricsSvmUserThroughput = Field(
        default_factory=OntapTopMetricsSvmUserThroughput
    )
    user_id: str = ""
    user_name: str = ""
    volumes: list[OntapTopMetricsSvmUserVolume] = Field(default_factory=list)
