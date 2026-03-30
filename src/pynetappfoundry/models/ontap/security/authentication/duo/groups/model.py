"""OntapDuogroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDuogroup(OntapModel):
    """OntapDuogroup information."""

    comment: str = ""
    excluded_users: list[str] = Field(default_factory=list)
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
