"""OntapWebauthnCredentials type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.webauthn.credentials.model import (
    OntapWebauthnCredentials,
)

ONTAPWEBAUTHNCREDENTIALS_MAPPING = TypeMapping(
    name="OntapWebauthnCredentials",
    model_class=OntapWebauthnCredentials,
    api_endpoint="/security/webauthn/credentials?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="creation_time",
        ),
        FieldMapping(
            cache_attr="credential.id_sha",
        ),
        FieldMapping(
            cache_attr="credential.type_",
            api_path="credential.type",
        ),
        FieldMapping(
            cache_attr="display_name",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="last_used_time",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="public_key.algorithm",
        ),
        FieldMapping(
            cache_attr="public_key.value",
        ),
        FieldMapping(
            cache_attr="relying_party.id",
        ),
        FieldMapping(
            cache_attr="relying_party.name",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="username",
        ),
    ),
)

model_registry.register_mapping("OntapWebauthnCredentials", ONTAPWEBAUTHNCREDENTIALS_MAPPING)
