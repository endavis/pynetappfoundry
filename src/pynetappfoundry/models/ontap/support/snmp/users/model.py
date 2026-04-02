"""OntapSnmpUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnmpUserOwner(OntapModel):
    """OntapSnmpUserOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapSnmpUserSnmpv3(OntapModel):
    """OntapSnmpUserSnmpv3 sub-model for snmpv3."""

    authentication_password: str = ""
    authentication_protocol: str = ""
    privacy_password: str = ""
    privacy_protocol: str = ""


class OntapSnmpUser(OntapModel):
    """OntapSnmpUser information."""

    authentication_method: str = ""
    comment: str = ""
    engine_id: str = ""
    name: str = ""
    owner: OntapSnmpUserOwner = Field(default_factory=OntapSnmpUserOwner)
    scope: str = ""
    snmpv3: OntapSnmpUserSnmpv3 = Field(default_factory=OntapSnmpUserSnmpv3)
    switch_address: str = ""
