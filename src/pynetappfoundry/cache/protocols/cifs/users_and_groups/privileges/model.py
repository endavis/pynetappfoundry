"""OntapUserGroupPrivileges information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapUserGroupPrivileges(CacheModel):
    """OntapUserGroupPrivileges information."""

    name: str = ""
    privileges: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
