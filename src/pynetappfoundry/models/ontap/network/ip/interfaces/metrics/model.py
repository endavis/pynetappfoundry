"""OntapInterfaceMetricsResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapInterfaceMetricsResponse(OntapModel):
    """OntapInterfaceMetricsResponse information."""

    duration: str = ""
    status: str = ""
    throughput_read: int = 0
    throughput_total: int = 0
    throughput_write: int = 0
    timestamp: str = ""
    uuid: str = ""
