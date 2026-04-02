"""OntapPortMetricsResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortMetricsResponseThroughput(OntapModel):
    """OntapPortMetricsResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapPortMetricsResponse(OntapModel):
    """OntapPortMetricsResponse information."""

    duration: str = ""
    status: str = ""
    throughput: OntapPortMetricsResponseThroughput = Field(
        default_factory=OntapPortMetricsResponseThroughput
    )
    timestamp: str = ""
    uuid: str = ""
