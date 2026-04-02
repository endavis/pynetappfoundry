"""OntapGroupRoleMappings information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupRoleMappingsOntapRole(OntapModel):
    """OntapGroupRoleMappingsOntapRole sub-model for ontap_role."""

    name: str = ""


class OntapGroupRoleMappings(OntapModel):
    """OntapGroupRoleMappings information."""

    comment: str = ""
    group_id: int = 0
    ontap_role: OntapGroupRoleMappingsOntapRole = Field(
        default_factory=OntapGroupRoleMappingsOntapRole
    )
    scope: str = ""
