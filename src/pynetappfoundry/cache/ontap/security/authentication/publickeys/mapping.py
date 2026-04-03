"""OntapPublickey type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.publickeys.model import OntapPublickey

ONTAPPUBLICKEY_MAPPING = TypeMapping(
    name="OntapPublickey",
    model_class=OntapPublickey,
    api_endpoint="/security/authentication/publickeys?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="account.name",
        ),
        FieldMapping(
            cache_attr="certificate",
        ),
        FieldMapping(
            cache_attr="certificate_details",
        ),
        FieldMapping(
            cache_attr="certificate_expired",
        ),
        FieldMapping(
            cache_attr="certificate_revoked",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="obfuscated_fingerprint",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="public_key",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="sha_fingerprint",
        ),
    ),
)

model_registry.register_mapping("OntapPublickey", ONTAPPUBLICKEY_MAPPING)
