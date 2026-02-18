"""OntapWwpnAlias information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapWwpnAlias(CacheModel):
    """OntapWwpnAlias information."""

    alias: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    wwpn: str = ""
