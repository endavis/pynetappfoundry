"""OntapConsistencyGroupMetricsResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapConsistencyGroupMetricsResponse(OntapModel):
    """OntapConsistencyGroupMetricsResponse information."""

    available_space: int = 0
    duration: str = ""
    iops_other: int = 0
    iops_read: int = 0
    iops_total: int = 0
    iops_write: int = 0
    latency_other: int = 0
    latency_read: int = 0
    latency_total: int = 0
    latency_write: int = 0
    size: int = 0
    status: str = ""
    throughput_other: int = 0
    throughput_read: int = 0
    throughput_total: int = 0
    throughput_write: int = 0
    timestamp: str = ""
    used_space: int = 0
