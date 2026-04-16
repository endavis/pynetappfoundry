# ruff: noqa: N815
"""DiiInvitesresponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiInvitesresponseApplicationrole(OntapModel):
    """DiiInvitesresponseApplicationrole sub-model for applicationRoles."""

    role: str = ""
    application: str = ""


class DiiInvitesresponse(OntapModel):
    """DiiInvitesresponse information."""

    expiration: str = ""
    id: str = ""
    email: str = ""
    applicationRoles: list[DiiInvitesresponseApplicationrole] = Field(default_factory=list)
