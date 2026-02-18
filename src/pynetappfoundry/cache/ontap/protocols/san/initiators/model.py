"""OntapInitiator information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapInitiator(CacheModel):
    """OntapInitiator information."""

    comment: str = ""
    name: str = ""
    protocol: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
