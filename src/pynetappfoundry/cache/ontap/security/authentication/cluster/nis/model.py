"""OntapClusterNisService information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapClusterNisService(CacheModel):
    """OntapClusterNisService information."""

    server: str = ""
    status_code: str = ""
    status_message: str = ""
