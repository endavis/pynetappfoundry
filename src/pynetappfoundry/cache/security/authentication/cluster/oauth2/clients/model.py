"""OntapSecurityOauth2 information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSecurityOauth2(CacheModel):
    """OntapSecurityOauth2 information."""

    application: str = ""
    audience: str = ""
    client_id: str = ""
    client_secret: str = ""
    hashed_client_secret: str = ""
    introspection_endpoint_uri: str = ""
    introspection_interval: str = ""
    issuer: str = ""
    jwks_provider_uri: str = ""
    jwks_refresh_interval: str = ""
    name: str = ""
    outgoing_proxy: str = ""
    provider: str = ""
    remote_user_claim: str = ""
    skip_uri_validation: bool = False
    use_local_roles_if_present: bool = False
    use_mutual_tls: str = ""
