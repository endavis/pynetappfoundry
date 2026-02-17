"""OntapPortMetricsResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapPortMetricsResponse(CacheModel):
    """OntapPortMetricsResponse information."""

    duration: str = ""
    status: str = ""
    throughput_read: int = 0
    throughput_total: int = 0
    throughput_write: int = 0
    timestamp: str = ""
    uuid: str = ""
