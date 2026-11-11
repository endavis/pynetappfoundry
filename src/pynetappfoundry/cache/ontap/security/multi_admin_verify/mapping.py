"""OntapMultiAdminVerifyConfig type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.multi_admin_verify.model import (
    OntapMultiAdminVerifyConfig,
)

ONTAPMULTIADMINVERIFYCONFIG_MAPPING = TypeMapping(
    name="OntapMultiAdminVerifyConfig",
    model_class=OntapMultiAdminVerifyConfig,
    api_endpoint="/security/multi-admin-verify?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="approval_expiry",
        ),
        FieldMapping(
            cache_attr="approval_groups",
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="execution_expiry",
        ),
        FieldMapping(
            cache_attr="required_approvers",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapMultiAdminVerifyConfig", ONTAPMULTIADMINVERIFYCONFIG_MAPPING)
