"""OntapGroupRoleMappings information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapGroupRoleMappings(CacheModel):
    """OntapGroupRoleMappings information."""

    comment: str = ""
    group_id: int = 0
    ontap_role_name: str = ""
    scope: str = ""
