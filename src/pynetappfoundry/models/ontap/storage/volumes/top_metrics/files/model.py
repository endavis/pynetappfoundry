"""OntapTopMetricsFile information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapTopMetricsFile(OntapModel):
    """OntapTopMetricsFile information."""

    iops_error_lower_bound: int = 0
    iops_error_upper_bound: int = 0
    iops_read: int = 0
    iops_write: int = 0
    path: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    throughput_error_lower_bound: int = 0
    throughput_error_upper_bound: int = 0
    throughput_read: int = 0
    throughput_write: int = 0
    volume_name: str = ""
    volume_uuid: str = ""
