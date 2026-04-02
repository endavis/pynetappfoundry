"""OntapSnmpTraphost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnmpTraphostUser(OntapModel):
    """OntapSnmpTraphostUser sub-model for user."""

    name: str = ""


class OntapSnmpTraphost(OntapModel):
    """OntapSnmpTraphost information."""

    host: str = ""
    ip_address: str = ""
    user: OntapSnmpTraphostUser = Field(default_factory=OntapSnmpTraphostUser)
