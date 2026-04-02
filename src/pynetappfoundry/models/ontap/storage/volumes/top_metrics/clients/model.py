"""OntapTopMetricsClient information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsClientIopsError(OntapModel):
    """OntapTopMetricsClientIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsClientIops(OntapModel):
    """OntapTopMetricsClientIops sub-model for iops."""

    error: OntapTopMetricsClientIopsError = Field(default_factory=OntapTopMetricsClientIopsError)
    read: int = 0
    write: int = 0


class OntapTopMetricsClientSvm(OntapModel):
    """OntapTopMetricsClientSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsClientThroughputError(OntapModel):
    """OntapTopMetricsClientThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsClientThroughput(OntapModel):
    """OntapTopMetricsClientThroughput sub-model for throughput."""

    error: OntapTopMetricsClientThroughputError = Field(
        default_factory=OntapTopMetricsClientThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsClientVolume(OntapModel):
    """OntapTopMetricsClientVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsClient(OntapModel):
    """OntapTopMetricsClient information."""

    client_ip: str = ""
    iops: OntapTopMetricsClientIops = Field(default_factory=OntapTopMetricsClientIops)
    svm: OntapTopMetricsClientSvm = Field(default_factory=OntapTopMetricsClientSvm)
    throughput: OntapTopMetricsClientThroughput = Field(
        default_factory=OntapTopMetricsClientThroughput
    )
    volume: OntapTopMetricsClientVolume = Field(default_factory=OntapTopMetricsClientVolume)
