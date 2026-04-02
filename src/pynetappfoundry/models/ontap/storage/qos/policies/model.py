"""OntapQosPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapQosPolicyAdaptive(OntapModel):
    """OntapQosPolicyAdaptive sub-model for adaptive."""

    absolute_min_iops: int = 0
    block_size: str = ""
    expected_iops: int = 0
    expected_iops_allocation: str = ""
    peak_iops: int = 0
    peak_iops_allocation: str = ""


class OntapQosPolicyFixed(OntapModel):
    """OntapQosPolicyFixed sub-model for fixed."""

    capacity_shared: bool = False
    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0


class OntapQosPolicySvm(OntapModel):
    """OntapQosPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapQosPolicy(OntapModel):
    """OntapQosPolicy information."""

    adaptive: OntapQosPolicyAdaptive = Field(default_factory=OntapQosPolicyAdaptive)
    fixed: OntapQosPolicyFixed = Field(default_factory=OntapQosPolicyFixed)
    name: str = ""
    object_count: int = 0
    pgid: int = 0
    policy_class: str = ""
    scope: str = ""
    svm: OntapQosPolicySvm = Field(default_factory=OntapQosPolicySvm)
    uuid: str = ""
