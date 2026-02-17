"""OntapPerformanceQtreeMetricResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapPerformanceQtreeMetricResponse(CacheModel):
    """OntapPerformanceQtreeMetricResponse information."""

    duration: str = ""
    iops_other: int = 0
    iops_read: int = 0
    iops_total: int = 0
    iops_write: int = 0
    latency_other: int = 0
    latency_read: int = 0
    latency_total: int = 0
    latency_write: int = 0
    qtree_id: int = 0
    qtree_name: str = ""
    status: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    throughput_other: int = 0
    throughput_read: int = 0
    throughput_total: int = 0
    throughput_write: int = 0
    timestamp: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
