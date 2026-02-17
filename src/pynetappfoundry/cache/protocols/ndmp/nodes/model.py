"""OntapNdmpNode information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNdmpNode(CacheModel):
    """OntapNdmpNode information."""

    authentication_types: list[str] = Field(default_factory=list)
    enabled: bool = False
    node_name: str = ""
    node_uuid: str = ""
    password: str = ""
    user: str = ""
