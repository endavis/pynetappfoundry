"""OntapKeyManagerAuthKey type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_managers.auth_keys.model import (
    OntapKeyManagerAuthKey,
)

ONTAPKEYMANAGERAUTHKEY_MAPPING = TypeMapping(
    name="OntapKeyManagerAuthKey",
    model_class=OntapKeyManagerAuthKey,
    api_endpoint="/security/key-managers/{security_key_manager.uuid}/auth-keys?fields=*",
    api_type="ontap",
    parent_mapping="OntapSecurityKeyManager",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="key_id",
            api_path="key_id",
        ),
        FieldMapping(
            cache_attr="key_tag",
            api_path="key_tag",
        ),
        FieldMapping(
            cache_attr="passphrase",
            api_path="passphrase",
        ),
        FieldMapping(
            cache_attr="security_key_manager.uuid",
            api_path="security_key_manager.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapKeyManagerAuthKey", ONTAPKEYMANAGERAUTHKEY_MAPPING)
