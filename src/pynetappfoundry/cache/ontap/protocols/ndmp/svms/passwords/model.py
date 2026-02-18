"""OntapNdmpPassword information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNdmpPassword(CacheModel):
    """OntapNdmpPassword information."""

    password: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    user: str = ""
