"""OntapSecurityGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSecurityGroupOwner(OntapModel):
    """OntapSecurityGroupOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapSecurityGroup(OntapModel):
    """OntapSecurityGroup information."""

    comment: str = ""
    create_time: str = ""
    id: int = 0
    name: str = ""
    owner: OntapSecurityGroupOwner = Field(default_factory=OntapSecurityGroupOwner)
    scope: str = ""
    type_: str = ""
    uuid: OntapUUID = ""
