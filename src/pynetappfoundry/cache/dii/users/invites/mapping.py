"""DiiInvitesresponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.users.invites.model import (
    DiiInvitesresponse,
    DiiInvitesresponseApplicationrole,
)

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
            item_model=DiiInvitesresponseApplicationrole,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiInvitesresponse", DIIINVITESRESPONSE_MAPPING)
