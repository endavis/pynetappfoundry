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
            api_path="creation_time",
        ),
        FieldMapping(
            cache_attr="credential.id_sha",
            api_path="credential.id_sha",
        ),
        FieldMapping(
            cache_attr="credential.type_",
            api_path="credential.type",
        ),
        FieldMapping(
            cache_attr="display_name",
            api_path="display_name",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="last_used_time",
            api_path="last_used_time",
        ),
        FieldMapping(
            cache_attr="owner.name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="public_key.algorithm",
            api_path="public_key.algorithm",
        ),
        FieldMapping(
            cache_attr="public_key.value",
            api_path="public_key.value",
        ),
        FieldMapping(
            cache_attr="relying_party.id",
            api_path="relying_party.id",
        ),
        FieldMapping(
            cache_attr="relying_party.name",
            api_path="relying_party.name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="username",
            api_path="username",
        ),
    ),
)

model_registry.register_mapping("OntapWebauthnCredentials", ONTAPWEBAUTHNCREDENTIALS_MAPPING)
