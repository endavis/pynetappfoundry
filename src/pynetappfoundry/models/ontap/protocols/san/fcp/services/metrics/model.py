"""OntapPerformanceFcpMetricResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceFcpMetricResponse(OntapModel):
    """OntapPerformanceFcpMetricResponse information."""

    duration: str = ""
    iops_other: int = 0
    iops_read: int = 0
    iops_total: int = 0
    iops_write: int = 0
    latency_other: int = 0
    latency_read: int = 0
    latency_total: int = 0
    latency_write: int = 0
    status: str = ""
    svm_uuid: str = ""
    throughput_read: int = 0
    throughput_total: int = 0
    throughput_write: int = 0
    timestamp: str = ""
