"""OntapDuogroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDuogroupOwner(OntapModel):
    """OntapDuogroupOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapDuogroup(OntapModel):
    """OntapDuogroup information."""

    comment: str = ""
    excluded_users: list[str] = Field(default_factory=list)
    name: str = ""
    owner: OntapDuogroupOwner = Field(default_factory=OntapDuogroupOwner)
