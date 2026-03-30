"""OntapFcZone information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcZoneMember(OntapModel):
    """OntapFcZoneMember sub-model for members."""

    members_name: str = ""
    members_type: str = ""


class OntapFcZone(OntapModel):
    """OntapFcZone information."""

    cache_age: str = ""
    cache_is_current: bool = False
    cache_update_time: str = ""
    fabric_name: str = ""
    members: list[OntapFcZoneMember] = Field(default_factory=list)
    name: str = ""
