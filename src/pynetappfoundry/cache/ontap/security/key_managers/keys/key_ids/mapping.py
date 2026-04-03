"""OntapKeyManagerKeys type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_managers.keys.key_ids.model import (
    OntapKeyManagerKeys,
)

ONTAPKEYMANAGERKEYS_MAPPING = TypeMapping(
    name="OntapKeyManagerKeys",
    model_class=OntapKeyManagerKeys,
    api_endpoint="/security/key-managers/{security_key_manager.uuid}/keys/{node.uuid}/key-ids?fields=*",
    api_type="ontap",
    parent_mapping="OntapSecurityKeyManager",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="crn",
        ),
        FieldMapping(
            cache_attr="encryption_algorithm",
        ),
        FieldMapping(
            cache_attr="key_id",
        ),
        FieldMapping(
            cache_attr="key_manager",
        ),
        FieldMapping(
            cache_attr="key_server",
        ),
        FieldMapping(
            cache_attr="key_store",
        ),
        FieldMapping(
            cache_attr="key_store_type",
        ),
        FieldMapping(
            cache_attr="key_tag",
        ),
        FieldMapping(
            cache_attr="key_type",
        ),
        FieldMapping(
            cache_attr="key_user",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="policy",
        ),
        FieldMapping(
            cache_attr="restored",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="security_key_manager.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapKeyManagerKeys", ONTAPKEYMANAGERKEYS_MAPPING)
