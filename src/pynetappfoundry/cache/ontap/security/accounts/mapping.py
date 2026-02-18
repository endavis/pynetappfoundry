"""OntapAccount type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.accounts.model import (
    OntapAccount,
    OntapAccountApplication,
)


def _transform_applications(record: dict[str, Any]) -> list[OntapAccountApplication]:
    """Transform applications into OntapAccountApplication list."""
    return [OntapAccountApplication(**item) for item in record.get("applications", [])]


ONTAPACCOUNT_MAPPING = TypeMapping(
    name="OntapAccount",
    model_class=OntapAccount,
    api_endpoint="/security/accounts?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="applications",
            transform=_transform_applications,
            default=[],
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="locked",
            api_path="locked",
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
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="password_hash_algorithm",
            api_path="password_hash_algorithm",
        ),
        FieldMapping(
            cache_attr="role_name",
            api_path="role.name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
    ),
)

model_registry.register_mapping("OntapAccount", ONTAPACCOUNT_MAPPING)
