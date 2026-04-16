# ruff: noqa: N802
"""DiiInvitesresponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.users.invites.model import (
    DiiInvitesresponse,
    DiiInvitesresponseApplicationrole,
)


def _transform_applicationRoles(record: dict[str, Any]) -> list[DiiInvitesresponseApplicationrole]:
    """Transform applicationRoles into DiiInvitesresponseApplicationrole list."""
    return [
        DiiInvitesresponseApplicationrole(**item) for item in record.get("applicationRoles", [])
    ]


DIIINVITESRESPONSE_MAPPING = TypeMapping(
    name="DiiInvitesresponse",
    model_class=DiiInvitesresponse,
    api_endpoint="/users/invites",
    api_type="dii",
    identifier_field="inviteId",
    records_path="invites",
    fields=(
        FieldMapping(
            cache_attr="expiration",
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

model_registry.register_mapping("DiiInvitesresponse", DIIINVITESRESPONSE_MAPPING)
