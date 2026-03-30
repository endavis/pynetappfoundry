"""OntapLocalHost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalHost(OntapModel):
    """OntapLocalHost information."""

    address: str = ""
    aliases: list[str] = Field(default_factory=list)
    hostname: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    scope: str = ""
