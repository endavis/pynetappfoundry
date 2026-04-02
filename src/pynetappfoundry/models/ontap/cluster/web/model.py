"""OntapWeb information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapWebCertificate(OntapModel):
    """OntapWebCertificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapWebCsrfToken(OntapModel):
    """OntapWebCsrfToken sub-model for token."""

    concurrent_limit: int = 0
    idle_timeout: int = 0
    max_timeout: int = 0


class OntapWebCsrf(OntapModel):
    """OntapWebCsrf sub-model for csrf."""

    protection_enabled: bool = False
    token: OntapWebCsrfToken = Field(default_factory=OntapWebCsrfToken)


class OntapWeb(OntapModel):
    """OntapWeb information."""

    certificate: OntapWebCertificate = Field(default_factory=OntapWebCertificate)
    client_enabled: bool = False
    csrf: OntapWebCsrf = Field(default_factory=OntapWebCsrf)
    enabled: bool = False
    http_enabled: bool = False
    http_port: int = 0
    https_port: int = 0
    ocsp_enabled: bool = False
    per_address_limit: int = 0
    state: str = ""
    wait_queue_capacity: int = 0
