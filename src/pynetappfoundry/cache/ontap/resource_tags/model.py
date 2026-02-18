"""OntapResourceTag information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapResourceTag(CacheModel):
    """OntapResourceTag information."""

    num_resources: int = 0
    value: str = ""
