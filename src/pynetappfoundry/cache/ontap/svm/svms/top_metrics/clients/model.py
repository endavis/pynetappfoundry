"""OntapTopMetricsSvmClient information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapTopMetricsSvmClient(CacheModel):
    """OntapTopMetricsSvmClient information."""

    client_ip: str = ""
    iops_error_lower_bound: int = 0
    iops_error_upper_bound: int = 0
    iops_read: int = 0
    iops_write: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    throughput_error_lower_bound: int = 0
    throughput_error_upper_bound: int = 0
    throughput_read: int = 0
    throughput_write: int = 0
