"""QoS policy information — /storage/qos/policies."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class QosPolicyInfo(CacheModel):
    """QoS policy information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    scope: str = ""  # cluster, svm
    policy_class: str = ""  # preset, user_defined, system_defined
    fixed_max_throughput_iops: int = 0
    fixed_max_throughput_mbps: int = 0
    adaptive_expected_iops: int = 0
    adaptive_peak_iops: int = 0
    adaptive_block_size: str = ""  # any, 4k, 8k, etc.
