"""OntapSoftwarePackage information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSoftwarePackage(CacheModel):
    """OntapSoftwarePackage information."""

    create_time: str = ""
    version: str = ""
