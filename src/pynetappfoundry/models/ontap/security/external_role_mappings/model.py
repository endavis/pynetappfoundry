"""OntapSecurityExternalRoleMapping information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSecurityExternalRoleMapping(OntapModel):
    """OntapSecurityExternalRoleMapping information."""

    comment: str = ""
    external_role: str = ""
    ontap_role_name: str = ""
    provider: str = ""
    timestamp: str = ""
