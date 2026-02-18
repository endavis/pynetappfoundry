"""OntapTopMetricsSvmUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapTopMetricsSvmUserVolume(CacheModel):
    """OntapTopMetricsSvmUserVolume sub-model for volumes."""

    volumes_name: str = ""
    volumes_uuid: str = ""


class OntapTopMetricsSvmUser(CacheModel):
    """OntapTopMetricsSvmUser information."""

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
    user_id: str = ""
    user_name: str = ""
    volumes: list[OntapTopMetricsSvmUserVolume] = Field(default_factory=list)
