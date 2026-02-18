"""OntapSecurityGroup information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapSecurityGroup(CacheModel):
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
