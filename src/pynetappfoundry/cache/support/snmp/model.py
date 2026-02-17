"""OntapSnmp information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnmp(CacheModel):
    """OntapSnmp information."""

    auth_traps_enabled: bool = False
    contact: str = ""
    enabled: bool = False
    location: str = ""
    traps_enabled: bool = False
    trigger_test_trap: bool = False
