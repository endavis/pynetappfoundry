"""OntapRolePrivilege type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.roles.privileges.model import OntapRolePrivilege

ONTAPROLEPRIVILEGE_MAPPING = TypeMapping(
    name="OntapRolePrivilege",
    model_class=OntapRolePrivilege,
    api_endpoint="/security/roles/{owner.uuid}/{name}/privileges?fields=*",
    api_type="ontap",
    parent_mapping="OntapRole",
    parent_id_field="owner_uuid",
    fields=(
        FieldMapping(
            cache_attr="access",
            api_path="access",
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="query",
            api_path="query",
        ),
    ),
)

model_registry.register_mapping("OntapRolePrivilege", ONTAPROLEPRIVILEGE_MAPPING)
