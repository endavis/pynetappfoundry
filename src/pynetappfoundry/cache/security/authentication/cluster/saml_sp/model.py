"""OntapSecuritySamlSp information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSecuritySamlSp(CacheModel):
    """OntapSecuritySamlSp information."""

    certificate_ca: str = ""
    certificate_common_name: str = ""
    certificate_serial_number: str = ""
    enabled: bool = False
    host: str = ""
    idp_uri: str = ""
