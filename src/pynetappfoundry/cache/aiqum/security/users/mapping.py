"""AiqumUser type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.security.users.model import AiqumUser

AIQUMUSER_MAPPING = TypeMapping(
    name="AiqumUser",
    model_class=AiqumUser,
    api_endpoint="/security/users",
    api_type="aiqum",
    identifier_field="name",
    fields=(
        FieldMapping(
            cache_attr="authentication_type",
        ),
        FieldMapping(
            cache_attr="confirm_password",
        ),
        FieldMapping(
            cache_attr="email",
        ),
        FieldMapping(
            cache_attr="group",
            default=False,
        ),
        FieldMapping(
            cache_attr="locked",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="role",
        ),
    ),
)

model_registry.register_mapping("AiqumUser", AIQUMUSER_MAPPING)
