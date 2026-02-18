"""OntapClusterAdProxy information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapClusterAdProxy(CacheModel):
    """OntapClusterAdProxy information."""

    svm_name: str = ""
    svm_uuid: str = ""
