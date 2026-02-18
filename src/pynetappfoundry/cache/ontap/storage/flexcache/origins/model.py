"""OntapFlexcacheOrigin information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapFlexcacheOrigin(CacheModel):
    """OntapFlexcacheOrigin information."""

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
