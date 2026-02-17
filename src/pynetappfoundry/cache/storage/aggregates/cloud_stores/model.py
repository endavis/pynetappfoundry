"""OntapCloudStore information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapCloudStore(CacheModel):
    """OntapCloudStore information."""

    aggregate_name: str = ""
    availability: str = ""
    availability_at_partner: str = ""
    mirror_degraded: bool = False
    primary: bool = False
    resync_progress: int = 0
    target_name: str = ""
    target_uuid: str = ""
    unavailable_reason_message: str = ""
    unreclaimed_space_threshold: int = 0
    used: int = 0
