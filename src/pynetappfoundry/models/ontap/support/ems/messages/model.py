"""OntapEmsMessageResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapEmsMessageResponse(OntapModel):
    """OntapEmsMessageResponse information."""

    corrective_action: str = ""
    deprecated: bool = False
    description: str = ""
    name: str = ""
    severity: str = ""
    snmp_trap_type: str = ""
