"""OntapSecurityExternalRoleMapping information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSecurityExternalRoleMapping(CacheModel):
    """OntapSecurityExternalRoleMapping information."""

    comment: str = ""
    external_role: str = ""
    ontap_role_name: str = ""
    provider: str = ""
    timestamp: str = ""
