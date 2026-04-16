# ruff: noqa: N802
"""DiiUsersresponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.users.model import DiiUsersresponse, DiiUsersresponseApplicationrole


def _transform_applicationRoles(record: dict[str, Any]) -> list[DiiUsersresponseApplicationrole]:
    """Transform applicationRoles into DiiUsersresponseApplicationrole list."""
    return [DiiUsersresponseApplicationrole(**item) for item in record.get("applicationRoles", [])]


DIIUSERSRESPONSE_MAPPING = TypeMapping(
    name="DiiUsersresponse",
    model_class=DiiUsersresponse,
    api_endpoint="/users",
    api_type="dii",
    identifier_field="userId",
    records_path="users",
    fields=(
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="email",
        ),
        FieldMapping(
            cache_attr="applicationRoles",
            transform=_transform_applicationRoles,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiUsersresponse", DIIUSERSRESPONSE_MAPPING)
