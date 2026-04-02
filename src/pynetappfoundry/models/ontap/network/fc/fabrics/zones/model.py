"""OntapFcZone information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcZoneCache(OntapModel):
    """OntapFcZoneCache sub-model for cache."""

    age: str = ""
    is_current: bool = False
    update_time: str = ""


class OntapFcZoneFabric(OntapModel):
    """OntapFcZoneFabric sub-model for fabric."""

    name: str = ""


class OntapFcZoneMember(OntapModel):
    """OntapFcZoneMember sub-model for members."""

    name: str = ""
    type_: str = ""


class OntapFcZone(OntapModel):
    """OntapFcZone information."""

    cache: OntapFcZoneCache = Field(default_factory=OntapFcZoneCache)
    fabric: OntapFcZoneFabric = Field(default_factory=OntapFcZoneFabric)
    members: list[OntapFcZoneMember] = Field(default_factory=list)
    name: str = ""
