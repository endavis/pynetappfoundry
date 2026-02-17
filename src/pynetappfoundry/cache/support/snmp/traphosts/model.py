"""OntapSnmpTraphost information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnmpTraphost(CacheModel):
    """OntapSnmpTraphost information."""

    host: str = ""
    ip_address: str = ""
    user_name: str = ""
