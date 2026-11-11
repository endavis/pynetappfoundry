"""DiiUsersresponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.users.model import DiiUsersresponse, DiiUsersresponseApplicationrole

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
            item_model=DiiUsersresponseApplicationrole,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiUsersresponse", DIIUSERSRESPONSE_MAPPING)
