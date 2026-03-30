"""OntapSecurityGroup information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSecurityGroup(OntapModel):
    """OntapSecurityGroup information."""

    comment: str = ""
    create_time: str = ""
    id: int = 0
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    scope: str = ""
    type_: str = ""
    uuid: OntapUUID = ""
