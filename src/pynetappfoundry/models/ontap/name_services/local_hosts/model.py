"""OntapLocalHost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalHostOwner(OntapModel):
    """OntapLocalHostOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapLocalHost(OntapModel):
    """OntapLocalHost information."""

    address: str = ""
    aliases: list[str] = Field(default_factory=list)
    hostname: str = ""
    owner: OntapLocalHostOwner = Field(default_factory=OntapLocalHostOwner)
    scope: str = ""
