"""OntapCifsSearchPath information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapCifsSearchPath(CacheModel):
    """OntapCifsSearchPath information."""

    index: int = 0
    path: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
