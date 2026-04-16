# ruff: noqa: N815
"""DiiUsersresponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiUsersresponseApplicationrole(OntapModel):
    """DiiUsersresponseApplicationrole sub-model for applicationRoles."""

    role: str = ""
    application: str = ""


class DiiUsersresponse(OntapModel):
    """DiiUsersresponse information."""

    name: str = ""
    id: str = ""
    email: str = ""
    applicationRoles: list[DiiUsersresponseApplicationrole] = Field(default_factory=list)
