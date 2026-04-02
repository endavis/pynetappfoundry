"""OntapSecurityAuditLogForward type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.audit.destinations.model import (
    OntapSecurityAuditLogForward,
)

ONTAPSECURITYAUDITLOGFORWARD_MAPPING = TypeMapping(
    name="OntapSecurityAuditLogForward",
    model_class=OntapSecurityAuditLogForward,
    api_endpoint="/security/audit/destinations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="address",
            api_path="address",
        ),
        FieldMapping(
            cache_attr="facility",
            api_path="facility",
        ),
        FieldMapping(
            cache_attr="hostname_format_override",
            api_path="hostname_format_override",
        ),
        FieldMapping(
            cache_attr="ipspace.name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="message_format",
            api_path="message_format",
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="timestamp_format_override",
            api_path="timestamp_format_override",
        ),
        FieldMapping(
            cache_attr="verify_server",
            api_path="verify_server",
            default=False,
        ),
    ),
)

model_registry.register_mapping(
    "OntapSecurityAuditLogForward", ONTAPSECURITYAUDITLOGFORWARD_MAPPING
)
