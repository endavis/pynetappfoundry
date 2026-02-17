"""OntapGroupMembershipSettings information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapGroupMembershipSettings(CacheModel):
    """OntapGroupMembershipSettings information."""

    enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    ttl: str = ""
