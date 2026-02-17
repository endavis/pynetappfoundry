"""OntapFcZone information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapFcZoneMember(CacheModel):
    """OntapFcZoneMember sub-model for members."""

    members_name: str = ""
    members_type: str = ""


class OntapFcZone(CacheModel):
    """OntapFcZone information."""

    cache_age: str = ""
    cache_is_current: bool = False
    cache_update_time: str = ""
    fabric_name: str = ""
    members: list[OntapFcZoneMember] = Field(default_factory=list)
    name: str = ""
