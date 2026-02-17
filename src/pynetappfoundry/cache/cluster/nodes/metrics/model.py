"""OntapNodeMetricsResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNodeMetricsResponse(CacheModel):
    """OntapNodeMetricsResponse information."""

    duration: str = ""
    processor_utilization: int = 0
    status: str = ""
    timestamp: str = ""
    uuid: str = ""
