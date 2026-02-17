"""OntapFpolicyPersistentStore information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapFpolicyPersistentStore(CacheModel):
    """OntapFpolicyPersistentStore information."""

    autosize_mode: str = ""
    name: str = ""
    size: int = 0
    svm_uuid: str = ""
    volume: str = ""
