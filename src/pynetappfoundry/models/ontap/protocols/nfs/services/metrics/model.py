"""OntapPerformanceSvmNfsResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapPerformanceSvmNfsResponse(OntapModel):
    """OntapPerformanceSvmNfsResponse information."""

    v3_duration: str = ""
    v3_iops_other: int = 0
    v3_iops_read: int = 0
    v3_iops_total: int = 0
    v3_iops_write: int = 0
    v3_latency_other: int = 0
    v3_latency_read: int = 0
    v3_latency_total: int = 0
    v3_latency_write: int = 0
    v3_status: str = ""
    v3_throughput_read: int = 0
    v3_throughput_total: int = 0
    v3_throughput_write: int = 0
    v3_timestamp: str = ""
    v4_duration: str = ""
    v4_iops_other: int = 0
    v4_iops_read: int = 0
    v4_iops_total: int = 0
    v4_iops_write: int = 0
    v4_latency_other: int = 0
    v4_latency_read: int = 0
    v4_latency_total: int = 0
    v4_latency_write: int = 0
    v4_status: str = ""
    v4_throughput_read: int = 0
    v4_throughput_total: int = 0
    v4_throughput_write: int = 0
    v4_timestamp: str = ""
    v41_duration: str = ""
    v41_iops_other: int = 0
    v41_iops_read: int = 0
    v41_iops_total: int = 0
    v41_iops_write: int = 0
    v41_latency_other: int = 0
    v41_latency_read: int = 0
    v41_latency_total: int = 0
    v41_latency_write: int = 0
    v41_status: str = ""
    v41_throughput_read: int = 0
    v41_throughput_total: int = 0
    v41_throughput_write: int = 0
    v41_timestamp: str = ""
