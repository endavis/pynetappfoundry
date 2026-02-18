"""OntapUnixGroupSettings information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapUnixGroupSettings(CacheModel):
    """OntapUnixGroupSettings information."""

    enabled: bool = False
    negative_cache_enabled: bool = False
    negative_ttl: str = ""
    propagation_enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    ttl: str = ""
