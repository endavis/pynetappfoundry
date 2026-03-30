"""OntapUnixGroup type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.unix_groups.model import (
    OntapUnixGroup,
    OntapUnixGroupUser,
)


def _transform_users(record: dict[str, Any]) -> list[OntapUnixGroupUser]:
    """Transform users into OntapUnixGroupUser list."""
    return [OntapUnixGroupUser(**item) for item in record.get("users", [])]


ONTAPUNIXGROUP_MAPPING = TypeMapping(
    name="OntapUnixGroup",
    model_class=OntapUnixGroup,
    api_endpoint="/name-services/unix-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="skip_name_validation",
            api_path="skip_name_validation",
            default=False,
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
            cache_attr="users",
            api_path="users",
            transform=_transform_users,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapUnixGroup", ONTAPUNIXGROUP_MAPPING)
