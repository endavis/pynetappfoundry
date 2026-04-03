"""OntapSecurityExternalRoleMapping type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.external_role_mappings.model import (
    OntapSecurityExternalRoleMapping,
)

ONTAPSECURITYEXTERNALROLEMAPPING_MAPPING = TypeMapping(
    name="OntapSecurityExternalRoleMapping",
    model_class=OntapSecurityExternalRoleMapping,
    api_endpoint="/security/external-role-mappings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="external_role",
        ),
        FieldMapping(
            cache_attr="ontap_role.name",
        ),
        FieldMapping(
            cache_attr="provider",
        ),
        FieldMapping(
            cache_attr="timestamp",
        ),
    ),
)

model_registry.register_mapping(
    "OntapSecurityExternalRoleMapping", ONTAPSECURITYEXTERNALROLEMAPPING_MAPPING
)
