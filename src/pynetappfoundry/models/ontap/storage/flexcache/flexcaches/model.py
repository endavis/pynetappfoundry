"""OntapFlexcache information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapFlexcacheAggregate(OntapModel):
    """OntapFlexcacheAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheOrigin(OntapModel):
    """OntapFlexcacheOrigin sub-model for origins."""

    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    create_time: str = ""
    ip_address: str = ""
    size: int = 0
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


class OntapFlexcache(OntapModel):
    """OntapFlexcache information."""

    aggregates: list[OntapFlexcacheAggregate] = Field(default_factory=list)
    atime_scrub_enabled: bool = False
    atime_scrub_period: int = 0
    cifs_change_notify_enabled: bool = False
    constituents_per_aggregate: int = 0
    dr_cache: bool = False
    global_file_locking_enabled: bool = False
    guarantee_type: str = ""
    name: str = ""
    origins: list[OntapFlexcacheOrigin] = Field(default_factory=list)
    override_encryption: bool = False
    path: str = ""
    prepopulate_dir_paths: list[str] = Field(default_factory=list)
    prepopulate_exclude_dir_paths: list[str] = Field(default_factory=list)
    prepopulate_recurse: bool = False
    relative_size_enabled: bool = False
    relative_size_percentage: int = 0
    size: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    use_tiered_aggregate: bool = False
    uuid: str = ""
    writeback_enabled: bool = False
