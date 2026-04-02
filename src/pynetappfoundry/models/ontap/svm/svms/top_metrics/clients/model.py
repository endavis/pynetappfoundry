"""OntapTopMetricsSvmClient information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsSvmClientIopsError(OntapModel):
    """OntapTopMetricsSvmClientIopsError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmClientIops(OntapModel):
    """OntapTopMetricsSvmClientIops sub-model for iops."""

    error: OntapTopMetricsSvmClientIopsError = Field(
        default_factory=OntapTopMetricsSvmClientIopsError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmClientSvm(OntapModel):
    """OntapTopMetricsSvmClientSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapTopMetricsSvmClientThroughputError(OntapModel):
    """OntapTopMetricsSvmClientThroughputError sub-model for error."""

    lower_bound: int = 0
    upper_bound: int = 0


class OntapTopMetricsSvmClientThroughput(OntapModel):
    """OntapTopMetricsSvmClientThroughput sub-model for throughput."""

    error: OntapTopMetricsSvmClientThroughputError = Field(
        default_factory=OntapTopMetricsSvmClientThroughputError
    )
    read: int = 0
    write: int = 0


class OntapTopMetricsSvmClient(OntapModel):
    """OntapTopMetricsSvmClient information."""

    client_ip: str = ""
    iops: OntapTopMetricsSvmClientIops = Field(default_factory=OntapTopMetricsSvmClientIops)
    svm: OntapTopMetricsSvmClientSvm = Field(default_factory=OntapTopMetricsSvmClientSvm)
    throughput: OntapTopMetricsSvmClientThroughput = Field(
        default_factory=OntapTopMetricsSvmClientThroughput
    )
