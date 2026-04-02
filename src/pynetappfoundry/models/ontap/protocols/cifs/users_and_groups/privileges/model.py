"""OntapUserGroupPrivileges information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUserGroupPrivilegesSvm(OntapModel):
    """OntapUserGroupPrivilegesSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapUserGroupPrivileges(OntapModel):
    """OntapUserGroupPrivileges information."""

    name: str = ""
    privileges: list[str] = Field(default_factory=list)
    svm: OntapUserGroupPrivilegesSvm = Field(default_factory=OntapUserGroupPrivilegesSvm)
