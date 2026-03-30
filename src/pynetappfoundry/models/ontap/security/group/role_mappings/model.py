"""OntapGroupRoleMappings information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapGroupRoleMappings(OntapModel):
    """OntapGroupRoleMappings information."""

    comment: str = ""
    group_id: int = 0
    ontap_role_name: str = ""
    scope: str = ""
