"""OntapDuogroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapDuogroup(CacheModel):
    """OntapDuogroup information."""

    comment: str = ""
    excluded_users: list[str] = Field(default_factory=list)
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
