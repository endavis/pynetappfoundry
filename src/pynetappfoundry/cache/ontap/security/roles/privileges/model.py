"""OntapRolePrivilege information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapRolePrivilege(CacheModel):
    """OntapRolePrivilege information."""

    access: str = ""
    path: str = ""
    query: str = ""
