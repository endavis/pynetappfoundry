"""OntapRole type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.roles.model import OntapRole, OntapRolePrivilege


def _transform_privileges(record: dict[str, Any]) -> list[OntapRolePrivilege]:
    """Transform privileges into OntapRolePrivilege list."""
    return [OntapRolePrivilege(**item) for item in record.get("privileges", [])]


ONTAPROLE_MAPPING = TypeMapping(
    name="OntapRole",
    model_class=OntapRole,
    api_endpoint="/security/roles?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="builtin",
            api_path="builtin",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
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
            cache_attr="privileges",
            api_path="privileges",
            transform=_transform_privileges,
            default=[],
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
    ),
)

model_registry.register_mapping("OntapRole", ONTAPROLE_MAPPING)
