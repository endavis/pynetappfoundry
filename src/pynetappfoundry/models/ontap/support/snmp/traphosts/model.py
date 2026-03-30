"""OntapSnmpTraphost information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSnmpTraphost(OntapModel):
    """OntapSnmpTraphost information."""

    host: str = ""
    ip_address: str = ""
    user_name: str = ""
