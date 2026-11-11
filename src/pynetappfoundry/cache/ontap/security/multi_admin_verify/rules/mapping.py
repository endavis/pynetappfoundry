"""OntapMultiAdminVerifyRule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.multi_admin_verify.rules.model import (
    OntapMultiAdminVerifyRule,
    OntapMultiAdminVerifyRuleApprovalGroup,
)

ONTAPMULTIADMINVERIFYRULE_MAPPING = TypeMapping(
    name="OntapMultiAdminVerifyRule",
    model_class=OntapMultiAdminVerifyRule,
    api_endpoint="/security/multi-admin-verify/rules?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="approval_expiry",
        ),
        FieldMapping(
            cache_attr="approval_groups",
            item_model=OntapMultiAdminVerifyRuleApprovalGroup,
            default=[],
        ),
        FieldMapping(
            cache_attr="auto_request_create",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="execution_expiry",
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
            cache_attr="query",
        ),
        FieldMapping(
            cache_attr="required_approvers",
            default=0,
        ),
        FieldMapping(
            cache_attr="system_defined",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapMultiAdminVerifyRule", ONTAPMULTIADMINVERIFYRULE_MAPPING)
