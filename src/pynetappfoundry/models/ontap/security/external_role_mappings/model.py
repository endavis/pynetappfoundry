"""OntapSecurityExternalRoleMapping information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityExternalRoleMappingOntapRole(OntapModel):
    """OntapSecurityExternalRoleMappingOntapRole sub-model for ontap_role."""

    name: str = ""


class OntapSecurityExternalRoleMapping(OntapModel):
    """OntapSecurityExternalRoleMapping information."""

    comment: str = ""
    external_role: str = ""
    ontap_role: OntapSecurityExternalRoleMappingOntapRole = Field(
        default_factory=OntapSecurityExternalRoleMappingOntapRole
    )
    provider: str = ""
    timestamp: str = ""
