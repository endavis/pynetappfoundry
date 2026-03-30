"""OntapMultiAdminVerifyRule type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.multi_admin_verify.rules.model import (
    OntapMultiAdminVerifyRule,
    OntapMultiAdminVerifyRuleApprovalGroup,
)


def _transform_approval_groups(
    record: dict[str, Any],
) -> list[OntapMultiAdminVerifyRuleApprovalGroup]:
    """Transform approval_groups into OntapMultiAdminVerifyRuleApprovalGroup list."""
    return [
        OntapMultiAdminVerifyRuleApprovalGroup(**item) for item in record.get("approval_groups", [])
    ]


ONTAPMULTIADMINVERIFYRULE_MAPPING = TypeMapping(
    name="OntapMultiAdminVerifyRule",
    model_class=OntapMultiAdminVerifyRule,
    api_endpoint="/security/multi-admin-verify/rules?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="approval_expiry",
            api_path="approval_expiry",
        ),
        FieldMapping(
            cache_attr="approval_groups",
            api_path="approval_groups",
            transform=_transform_approval_groups,
            default=[],
        ),
        FieldMapping(
            cache_attr="auto_request_create",
            api_path="auto_request_create",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="execution_expiry",
            api_path="execution_expiry",
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
            cache_attr="query",
            api_path="query",
        ),
        FieldMapping(
            cache_attr="required_approvers",
            api_path="required_approvers",
            default=0,
        ),
        FieldMapping(
            cache_attr="system_defined",
            api_path="system_defined",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapMultiAdminVerifyRule", ONTAPMULTIADMINVERIFYRULE_MAPPING)
