"""OntapNameMapping information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNameMapping(CacheModel):
    """OntapNameMapping information."""

    client_match: str = ""
    direction: str = ""
    index: int = 0
    pattern: str = ""
    replacement: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
