"""OntapIpspace information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapIpspace(CacheModel):
    """OntapIpspace information."""

    name: str = ""
    uuid: str = ""
