"""OntapGlobalCacheSetting information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapGlobalCacheSetting(OntapModel):
    """OntapGlobalCacheSetting information."""

    eviction_time_interval: str = ""
    remote_fetch_enabled: bool = False
