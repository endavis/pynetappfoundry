"""OntapSecurityKeystore type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_stores.model import OntapSecurityKeystore

ONTAPSECURITYKEYSTORE_MAPPING = TypeMapping(
    name="OntapSecurityKeystore",
    model_class=OntapSecurityKeystore,
    api_endpoint="/security/key-stores?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="configuration.name",
        ),
        FieldMapping(
            cache_attr="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityKeystore", ONTAPSECURITYKEYSTORE_MAPPING)
