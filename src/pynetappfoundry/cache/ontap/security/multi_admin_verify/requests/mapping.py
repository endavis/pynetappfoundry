"""OntapMultiAdminVerifyRequest type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.multi_admin_verify.requests.model import (
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
            api_path="approve_expiry_time",
        ),
        FieldMapping(
            cache_attr="approve_time",
            api_path="approve_time",
        ),
        FieldMapping(
            cache_attr="approved_users",
            api_path="approved_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="execute_on_approval",
            api_path="execute_on_approval",
            default=False,
        ),
        FieldMapping(
            cache_attr="execution_expiry_time",
            api_path="execution_expiry_time",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="operation",
            api_path="operation",
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
            cache_attr="pending_approvers",
            api_path="pending_approvers",
            default=0,
        ),
        FieldMapping(
            cache_attr="permitted_users",
            api_path="permitted_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="potential_approvers",
            api_path="potential_approvers",
            default=[],
        ),
        FieldMapping(
            cache_attr="query",
            api_path="query",
        ),
        FieldMapping(
            cache_attr="required_approvers",
            api_path="required_approvers",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="user_requested",
            api_path="user_requested",
        ),
        FieldMapping(
            cache_attr="user_vetoed",
            api_path="user_vetoed",
        ),
    ),
)

model_registry.register_mapping(
    "OntapMultiAdminVerifyRequest", ONTAPMULTIADMINVERIFYREQUEST_MAPPING
)
