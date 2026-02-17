"""OntapLocalHost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLocalHost(CacheModel):
    """OntapLocalHost information."""

    address: str = ""
    aliases: list[str] = Field(default_factory=list)
    hostname: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    scope: str = ""
