"""OntapUnixGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapUnixGroupUser(CacheModel):
    """OntapUnixGroupUser sub-model for users."""

    users_name: str = ""


class OntapUnixGroup(CacheModel):
    """OntapUnixGroup information."""

    id: int = 0
    name: str = ""
    skip_name_validation: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    users: list[OntapUnixGroupUser] = Field(default_factory=list)
