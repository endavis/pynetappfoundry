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
            cache_attr="configuration_name",
            api_path="configuration.name",
        ),
        FieldMapping(
            cache_attr="configuration_uuid",
            api_path="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityKeystore", ONTAPSECURITYKEYSTORE_MAPPING)
