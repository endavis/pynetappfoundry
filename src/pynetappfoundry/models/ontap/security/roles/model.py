"""OntapRole information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapRoleOwner(OntapModel):
    """OntapRoleOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapRolePrivilege(OntapModel):
    """OntapRolePrivilege sub-model for privileges."""

    access: str = ""
    path: str = ""
    query: str = ""


class OntapRole(OntapModel):
    """OntapRole information."""

    builtin: bool = False
    name: str = ""
    owner: OntapRoleOwner = Field(default_factory=OntapRoleOwner)
    privileges: list[OntapRolePrivilege] = Field(default_factory=list)
    scope: str = ""
