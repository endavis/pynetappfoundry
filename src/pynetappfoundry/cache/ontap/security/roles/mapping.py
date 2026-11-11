"""OntapRole type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.roles.model import OntapRole, OntapRolePrivilege

ONTAPROLE_MAPPING = TypeMapping(
    name="OntapRole",
    model_class=OntapRole,
    api_endpoint="/security/roles?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="builtin",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="privileges",
            item_model=OntapRolePrivilege,
            default=[],
        ),
        FieldMapping(
            cache_attr="scope",
        ),
    ),
)

model_registry.register_mapping("OntapRole", ONTAPROLE_MAPPING)
