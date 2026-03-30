"""OntapGroupRoleMappings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.group.role_mappings.model import OntapGroupRoleMappings

ONTAPGROUPROLEMAPPINGS_MAPPING = TypeMapping(
    name="OntapGroupRoleMappings",
    model_class=OntapGroupRoleMappings,
    api_endpoint="/security/group/role-mappings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="group_id",
            api_path="group_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="ontap_role_name",
            api_path="ontap_role.name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
    ),
)

model_registry.register_mapping("OntapGroupRoleMappings", ONTAPGROUPROLEMAPPINGS_MAPPING)
