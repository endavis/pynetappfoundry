"""OntapRole information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapRolePrivilege(CacheModel):
    """OntapRolePrivilege sub-model for privileges."""

    privileges_access: str = ""
    privileges_path: str = ""
    privileges_query: str = ""


class OntapRole(CacheModel):
    """OntapRole information."""

    builtin: bool = False
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    privileges: list[OntapRolePrivilege] = Field(default_factory=list)
    scope: str = ""
