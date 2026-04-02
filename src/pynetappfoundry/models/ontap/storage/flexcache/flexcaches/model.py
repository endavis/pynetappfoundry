"""OntapFlexcache information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapFlexcacheAggregate(OntapModel):
    """OntapFlexcacheAggregate sub-model for aggregates."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheAtimeScrub(OntapModel):
    """OntapFlexcacheAtimeScrub sub-model for atime_scrub."""

    enabled: bool = False
    period: int = 0


class OntapFlexcacheCifsChangeNotify(OntapModel):
    """OntapFlexcacheCifsChangeNotify sub-model for cifs_change_notify."""

    enabled: bool = False


class OntapFlexcacheGuarantee(OntapModel):
    """OntapFlexcacheGuarantee sub-model for guarantee."""

    type_: str = ""


class OntapFlexcacheOriginCluster(OntapModel):
    """OntapFlexcacheOriginCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapFlexcacheOriginSvm(OntapModel):
    """OntapFlexcacheOriginSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheOriginVolume(OntapModel):
    """OntapFlexcacheOriginVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheOrigin(OntapModel):
    """OntapFlexcacheOrigin sub-model for origins."""

    cluster: OntapFlexcacheOriginCluster = Field(default_factory=OntapFlexcacheOriginCluster)
    create_time: str = ""
    ip_address: str = ""
    size: int = 0
    state: str = ""
    svm: OntapFlexcacheOriginSvm = Field(default_factory=OntapFlexcacheOriginSvm)
    volume: OntapFlexcacheOriginVolume = Field(default_factory=OntapFlexcacheOriginVolume)


class OntapFlexcachePrepopulate(OntapModel):
    """OntapFlexcachePrepopulate sub-model for prepopulate."""

    dir_paths: list[str] = Field(default_factory=list)
    exclude_dir_paths: list[str] = Field(default_factory=list)
    recurse: bool = False


class OntapFlexcacheRelativeSize(OntapModel):
    """OntapFlexcacheRelativeSize sub-model for relative_size."""

    enabled: bool = False
    percentage: int = 0


class OntapFlexcacheSvm(OntapModel):
    """OntapFlexcacheSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheWriteback(OntapModel):
    """OntapFlexcacheWriteback sub-model for writeback."""

    enabled: bool = False


class OntapFlexcache(OntapModel):
    """OntapFlexcache information."""

    aggregates: list[OntapFlexcacheAggregate] = Field(default_factory=list)
    atime_scrub: OntapFlexcacheAtimeScrub = Field(default_factory=OntapFlexcacheAtimeScrub)
    cifs_change_notify: OntapFlexcacheCifsChangeNotify = Field(
        default_factory=OntapFlexcacheCifsChangeNotify
    )
    constituents_per_aggregate: int = 0
    dr_cache: bool = False
    global_file_locking_enabled: bool = False
    guarantee: OntapFlexcacheGuarantee = Field(default_factory=OntapFlexcacheGuarantee)
    name: str = ""
    origins: list[OntapFlexcacheOrigin] = Field(default_factory=list)
    override_encryption: bool = False
    path: str = ""
    prepopulate: OntapFlexcachePrepopulate = Field(default_factory=OntapFlexcachePrepopulate)
    relative_size: OntapFlexcacheRelativeSize = Field(default_factory=OntapFlexcacheRelativeSize)
    size: int = 0
    svm: OntapFlexcacheSvm = Field(default_factory=OntapFlexcacheSvm)
    use_tiered_aggregate: bool = False
    uuid: str = ""
    writeback: OntapFlexcacheWriteback = Field(default_factory=OntapFlexcacheWriteback)
