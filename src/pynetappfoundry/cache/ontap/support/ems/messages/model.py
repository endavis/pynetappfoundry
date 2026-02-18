"""OntapEmsMessageResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapEmsMessageResponse(CacheModel):
    """OntapEmsMessageResponse information."""

    corrective_action: str = ""
    deprecated: bool = False
    description: str = ""
    name: str = ""
    severity: str = ""
    snmp_trap_type: str = ""
