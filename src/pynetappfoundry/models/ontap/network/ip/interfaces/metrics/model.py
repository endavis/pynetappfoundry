"""OntapInterfaceMetricsResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapInterfaceMetricsResponseThroughput(OntapModel):
    """OntapInterfaceMetricsResponseThroughput sub-model for throughput."""

    read: int = 0
    total: int = 0
    write: int = 0


class OntapInterfaceMetricsResponse(OntapModel):
    """OntapInterfaceMetricsResponse information."""

    duration: str = ""
    status: str = ""
    throughput: OntapInterfaceMetricsResponseThroughput = Field(
        default_factory=OntapInterfaceMetricsResponseThroughput
    )
    timestamp: str = ""
    uuid: str = ""
