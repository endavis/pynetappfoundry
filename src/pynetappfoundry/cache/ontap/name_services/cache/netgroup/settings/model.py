"""OntapNetgroupsSettings information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNetgroupsSettings(CacheModel):
    """OntapNetgroupsSettings information."""

    enabled: bool = False
    negative_cache_enabled_byhost: bool = False
    negative_ttl_byhost: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    ttl_byhost: str = ""
    ttl_for_members: str = ""
