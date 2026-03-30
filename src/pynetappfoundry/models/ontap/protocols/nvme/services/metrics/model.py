"""OntapPerformanceNvmeMetricResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceNvmeMetricResponse(OntapModel):
    """OntapPerformanceNvmeMetricResponse information."""

    duration: str = ""
    fc_duration: str = ""
    fc_iops_other: int = 0
    fc_iops_read: int = 0
    fc_iops_total: int = 0
    fc_iops_write: int = 0
    fc_latency_other: int = 0
    fc_latency_read: int = 0
    fc_latency_total: int = 0
    fc_latency_write: int = 0
    fc_status: str = ""
    fc_throughput_read: int = 0
    fc_throughput_total: int = 0
    fc_throughput_write: int = 0
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
    tcp_duration: str = ""
    tcp_iops_other: int = 0
    tcp_iops_read: int = 0
    tcp_iops_total: int = 0
    tcp_iops_write: int = 0
    tcp_latency_other: int = 0
    tcp_latency_read: int = 0
    tcp_latency_total: int = 0
    tcp_latency_write: int = 0
    tcp_status: str = ""
    tcp_throughput_read: int = 0
    tcp_throughput_total: int = 0
    tcp_throughput_write: int = 0
    throughput_read: int = 0
    throughput_total: int = 0
    throughput_write: int = 0
    timestamp: str = ""
