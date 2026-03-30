"""OntapRolePrivilege information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapRolePrivilege(OntapModel):
    """OntapRolePrivilege information."""

    access: str = ""
    path: str = ""
    query: str = ""
