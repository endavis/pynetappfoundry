"""OntapLunAttribute information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapLunAttribute(CacheModel):
    """OntapLunAttribute information."""

    lun_uuid: str = ""
    name: str = ""
    value: str = ""
