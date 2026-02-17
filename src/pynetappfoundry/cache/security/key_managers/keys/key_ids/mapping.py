"""OntapKeyManagerKeys type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.key_managers.keys.key_ids.model import OntapKeyManagerKeys

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
            api_path="crn",
        ),
        FieldMapping(
            cache_attr="encryption_algorithm",
            api_path="encryption_algorithm",
        ),
        FieldMapping(
            cache_attr="key_id",
            api_path="key_id",
        ),
        FieldMapping(
            cache_attr="key_manager",
            api_path="key_manager",
        ),
        FieldMapping(
            cache_attr="key_server",
            api_path="key_server",
        ),
        FieldMapping(
            cache_attr="key_store",
            api_path="key_store",
        ),
        FieldMapping(
            cache_attr="key_store_type",
            api_path="key_store_type",
        ),
        FieldMapping(
            cache_attr="key_tag",
            api_path="key_tag",
        ),
        FieldMapping(
            cache_attr="key_type",
            api_path="key_type",
        ),
        FieldMapping(
            cache_attr="key_user",
            api_path="key_user",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="policy",
            api_path="policy",
        ),
        FieldMapping(
            cache_attr="restored",
            api_path="restored",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="security_key_manager_uuid",
            api_path="security_key_manager.uuid",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapKeyManagerKeys", ONTAPKEYMANAGERKEYS_MAPPING)
