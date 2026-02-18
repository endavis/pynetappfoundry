"""OntapUnixGroupUsers information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapUnixGroupUsersRecord(CacheModel):
    """OntapUnixGroupUsersRecord sub-model for records."""

    records_name: str = ""


class OntapUnixGroupUsers(CacheModel):
    """OntapUnixGroupUsers information."""

    name: str = ""
    records: list[OntapUnixGroupUsersRecord] = Field(default_factory=list)
    skip_name_validation: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    unix_group_name: str = ""
