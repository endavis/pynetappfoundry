"""OntapSecurityAudit type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.audit.model import OntapSecurityAudit

ONTAPSECURITYAUDIT_MAPPING = TypeMapping(
    name="OntapSecurityAudit",
    model_class=OntapSecurityAudit,
    api_endpoint="/security/audit?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cli",
            api_path="cli",
            default=False,
        ),
        FieldMapping(
            cache_attr="http",
            api_path="http",
            default=False,
        ),
        FieldMapping(
            cache_attr="ontapi",
            api_path="ontapi",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSecurityAudit", ONTAPSECURITYAUDIT_MAPPING)
