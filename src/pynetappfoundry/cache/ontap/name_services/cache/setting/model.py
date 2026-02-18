"""OntapGlobalCacheSetting information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapGlobalCacheSetting(CacheModel):
    """OntapGlobalCacheSetting information."""

    eviction_time_interval: str = ""
    remote_fetch_enabled: bool = False
