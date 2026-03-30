"""OntapSecurityOauth2 type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.cluster.oauth2.clients.model import (
    OntapSecurityOauth2,
)

ONTAPSECURITYOAUTH2_MAPPING = TypeMapping(
    name="OntapSecurityOauth2",
    model_class=OntapSecurityOauth2,
    api_endpoint="/security/authentication/cluster/oauth2/clients?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="application",
            api_path="application",
        ),
        FieldMapping(
            cache_attr="audience",
            api_path="audience",
        ),
        FieldMapping(
            cache_attr="client_id",
            api_path="client_id",
        ),
        FieldMapping(
            cache_attr="client_secret",
            api_path="client_secret",
        ),
        FieldMapping(
            cache_attr="hashed_client_secret",
            api_path="hashed_client_secret",
        ),
        FieldMapping(
            cache_attr="introspection_endpoint_uri",
            api_path="introspection.endpoint_uri",
        ),
        FieldMapping(
            cache_attr="introspection_interval",
            api_path="introspection.interval",
        ),
        FieldMapping(
            cache_attr="issuer",
            api_path="issuer",
        ),
        FieldMapping(
            cache_attr="jwks_provider_uri",
            api_path="jwks.provider_uri",
        ),
        FieldMapping(
            cache_attr="jwks_refresh_interval",
            api_path="jwks.refresh_interval",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="outgoing_proxy",
            api_path="outgoing_proxy",
        ),
        FieldMapping(
            cache_attr="provider",
            api_path="provider",
        ),
        FieldMapping(
            cache_attr="remote_user_claim",
            api_path="remote_user_claim",
        ),
        FieldMapping(
            cache_attr="skip_uri_validation",
            api_path="skip_uri_validation",
            default=False,
        ),
        FieldMapping(
            cache_attr="use_local_roles_if_present",
            api_path="use_local_roles_if_present",
            default=False,
        ),
        FieldMapping(
            cache_attr="use_mutual_tls",
            api_path="use_mutual_tls",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityOauth2", ONTAPSECURITYOAUTH2_MAPPING)
