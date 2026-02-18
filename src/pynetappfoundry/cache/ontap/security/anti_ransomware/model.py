"""OntapAntiRansomware information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapAntiRansomware(CacheModel):
    """OntapAntiRansomware information."""

    name: str = ""
    version: str = ""
