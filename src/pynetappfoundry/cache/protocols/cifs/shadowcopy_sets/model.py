"""OntapShadowcopySet information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapShadowcopySet(CacheModel):
    """OntapShadowcopySet information."""

    keep_snapshots: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
