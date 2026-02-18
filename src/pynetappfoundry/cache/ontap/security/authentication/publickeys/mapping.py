"""OntapPublickey type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.authentication.publickeys.model import OntapPublickey

ONTAPPUBLICKEY_MAPPING = TypeMapping(
    name="OntapPublickey",
    model_class=OntapPublickey,
    api_endpoint="/security/authentication/publickeys?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="account_name",
            api_path="account.name",
        ),
        FieldMapping(
            cache_attr="certificate",
            api_path="certificate",
        ),
        FieldMapping(
            cache_attr="certificate_details",
            api_path="certificate_details",
        ),
        FieldMapping(
            cache_attr="certificate_expired",
            api_path="certificate_expired",
        ),
        FieldMapping(
            cache_attr="certificate_revoked",
            api_path="certificate_revoked",
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="obfuscated_fingerprint",
            api_path="obfuscated_fingerprint",
        ),
        FieldMapping(
            cache_attr="owner_name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner_uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="public_key",
            api_path="public_key",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="sha_fingerprint",
            api_path="sha_fingerprint",
        ),
    ),
)

model_registry.register_mapping("OntapPublickey", ONTAPPUBLICKEY_MAPPING)
