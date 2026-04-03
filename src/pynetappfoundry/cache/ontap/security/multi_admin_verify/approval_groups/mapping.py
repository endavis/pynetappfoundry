"""OntapMultiAdminVerifyApprovalGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.multi_admin_verify.approval_groups.model import (
    OntapMultiAdminVerifyApprovalGroup,
)

ONTAPMULTIADMINVERIFYAPPROVALGROUP_MAPPING = TypeMapping(
    name="OntapMultiAdminVerifyApprovalGroup",
    model_class=OntapMultiAdminVerifyApprovalGroup,
    api_endpoint="/security/multi-admin-verify/approval-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="approvers",
            default=[],
        ),
        FieldMapping(
            cache_attr="email",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapMultiAdminVerifyApprovalGroup", ONTAPMULTIADMINVERIFYAPPROVALGROUP_MAPPING
)
