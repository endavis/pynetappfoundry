"""OntapQosPolicy information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapQosPolicy(OntapModel):
    """OntapQosPolicy information."""

    adaptive_absolute_min_iops: int = 0
    adaptive_block_size: str = ""
    adaptive_expected_iops: int = 0
    adaptive_expected_iops_allocation: str = ""
    adaptive_peak_iops: int = 0
    adaptive_peak_iops_allocation: str = ""
    fixed_capacity_shared: bool = False
    fixed_max_throughput_iops: int = 0
    fixed_max_throughput_mbps: int = 0
    fixed_min_throughput_iops: int = 0
    fixed_min_throughput_mbps: int = 0
    name: str = ""
    object_count: int = 0
    pgid: int = 0
    policy_class: str = ""
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
