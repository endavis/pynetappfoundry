"""OntapMultiAdminVerifyRequest type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.multi_admin_verify.requests.model import (
    OntapMultiAdminVerifyRequest,
)

ONTAPMULTIADMINVERIFYREQUEST_MAPPING = TypeMapping(
    name="OntapMultiAdminVerifyRequest",
    model_class=OntapMultiAdminVerifyRequest,
    api_endpoint="/security/multi-admin-verify/requests?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="approve_expiry_time",
        ),
        FieldMapping(
            cache_attr="approve_time",
        ),
        FieldMapping(
            cache_attr="approved_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="execute_on_approval",
            default=False,
        ),
        FieldMapping(
            cache_attr="execution_expiry_time",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="operation",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="pending_approvers",
            default=0,
        ),
        FieldMapping(
            cache_attr="permitted_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="potential_approvers",
            default=[],
        ),
        FieldMapping(
            cache_attr="query",
        ),
        FieldMapping(
            cache_attr="required_approvers",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="user_requested",
        ),
        FieldMapping(
            cache_attr="user_vetoed",
        ),
    ),
)

model_registry.register_mapping(
    "OntapMultiAdminVerifyRequest", ONTAPMULTIADMINVERIFYREQUEST_MAPPING
)
