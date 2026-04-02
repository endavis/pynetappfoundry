"""OntapSecurityOauth2 information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityOauth2Introspection(OntapModel):
    """OntapSecurityOauth2Introspection sub-model for introspection."""

    endpoint_uri: str = ""
    interval: str = ""


class OntapSecurityOauth2Jwks(OntapModel):
    """OntapSecurityOauth2Jwks sub-model for jwks."""

    provider_uri: str = ""
    refresh_interval: str = ""


class OntapSecurityOauth2(OntapModel):
    """OntapSecurityOauth2 information."""

    application: str = ""
    audience: str = ""
    client_id: str = ""
    client_secret: str = ""
    hashed_client_secret: str = ""
    introspection: OntapSecurityOauth2Introspection = Field(
        default_factory=OntapSecurityOauth2Introspection
    )
    issuer: str = ""
    jwks: OntapSecurityOauth2Jwks = Field(default_factory=OntapSecurityOauth2Jwks)
    name: str = ""
    outgoing_proxy: str = ""
    provider: str = ""
    remote_user_claim: str = ""
    skip_uri_validation: bool = False
    use_local_roles_if_present: bool = False
    use_mutual_tls: str = ""
