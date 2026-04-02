"""OntapTopMetricsUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsUserIopsError(OntapModel):
    """OntapTopMetricsUserIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsUserIops(OntapModel):
    """OntapTopMetricsUserIops sub-model for iops."""

    error: OntapTopMetricsUserIopsError = Field(default_factory=OntapTopMetricsUserIopsError)
    read: int = 0
    write: int = 0


class OntapTopMetricsUserSvm(OntapModel):
    """OntapTopMetricsUserSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsUserThroughputError(OntapModel):
    """OntapTopMetricsUserThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsUserThroughput(OntapModel):
    """OntapTopMetricsUserThroughput sub-model for throughput."""

    error: OntapTopMetricsUserThroughputError = Field(
        default_factory=OntapTopMetricsUserThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsUserVolume(OntapModel):
    """OntapTopMetricsUserVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsUser(OntapModel):
    """OntapTopMetricsUser information."""

    iops: OntapTopMetricsUserIops = Field(default_factory=OntapTopMetricsUserIops)
    svm: OntapTopMetricsUserSvm = Field(default_factory=OntapTopMetricsUserSvm)
    throughput: OntapTopMetricsUserThroughput = Field(default_factory=OntapTopMetricsUserThroughput)
    user_id: str = ""
    user_name: str = ""
    volume: OntapTopMetricsUserVolume = Field(default_factory=OntapTopMetricsUserVolume)
