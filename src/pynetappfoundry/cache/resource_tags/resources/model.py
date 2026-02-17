"""OntapResourceTagResource information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapResourceTagResource(CacheModel):
    """OntapResourceTagResource information."""

    href: str = ""
    label: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    value: str = ""
