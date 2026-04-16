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
    identifier_field="name",
    fields=(
        FieldMapping(
            cache_attr="application",
        ),
        FieldMapping(
            cache_attr="audience",
        ),
        FieldMapping(
            cache_attr="client_id",
        ),
        FieldMapping(
            cache_attr="client_secret",
        ),
        FieldMapping(
            cache_attr="hashed_client_secret",
        ),
        FieldMapping(
            cache_attr="introspection.endpoint_uri",
        ),
        FieldMapping(
            cache_attr="introspection.interval",
        ),
        FieldMapping(
            cache_attr="issuer",
        ),
        FieldMapping(
            cache_attr="jwks.provider_uri",
        ),
        FieldMapping(
            cache_attr="jwks.refresh_interval",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="outgoing_proxy",
        ),
        FieldMapping(
            cache_attr="provider",
        ),
        FieldMapping(
            cache_attr="remote_user_claim",
        ),
        FieldMapping(
            cache_attr="skip_uri_validation",
            default=False,
        ),
        FieldMapping(
            cache_attr="use_local_roles_if_present",
            default=False,
        ),
        FieldMapping(
            cache_attr="use_mutual_tls",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityOauth2", ONTAPSECURITYOAUTH2_MAPPING)
