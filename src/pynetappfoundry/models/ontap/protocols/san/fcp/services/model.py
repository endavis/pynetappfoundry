"""OntapFcpService information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapFcpService(OntapModel):
    """OntapFcpService information."""

    enabled: bool = False
    metric_duration: str = ""
    metric_iops_other: int = 0
    metric_iops_read: int = 0
    metric_iops_total: int = 0
    metric_iops_write: int = 0
    metric_latency_other: int = 0
    metric_latency_read: int = 0
    metric_latency_total: int = 0
    metric_latency_write: int = 0
    metric_status: str = ""
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    target_name: str = ""
