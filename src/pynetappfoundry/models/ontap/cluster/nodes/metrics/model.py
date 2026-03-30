"""OntapNodeMetricsResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNodeMetricsResponse(OntapModel):
    """OntapNodeMetricsResponse information."""

    duration: str = ""
    processor_utilization: int = 0
    status: str = ""
    timestamp: str = ""
    uuid: str = ""
