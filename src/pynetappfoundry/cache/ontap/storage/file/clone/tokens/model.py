"""OntapToken information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapToken(CacheModel):
    """OntapToken information."""

    expiry_time_left: str = ""
    expiry_time_limit: str = ""
    node_name: str = ""
    node_uuid: str = ""
    reserve_size: int = 0
    uuid: str = ""
