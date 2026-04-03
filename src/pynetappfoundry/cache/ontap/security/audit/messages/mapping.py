"""OntapSecurityAuditLog type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.audit.messages.model import OntapSecurityAuditLog

ONTAPSECURITYAUDITLOG_MAPPING = TypeMapping(
    name="OntapSecurityAuditLog",
    model_class=OntapSecurityAuditLog,
    api_endpoint="/security/audit/messages?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="application",
        ),
        FieldMapping(
            cache_attr="command_id",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="input",
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="message",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="session_id",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="timestamp",
        ),
        FieldMapping(
            cache_attr="user",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityAuditLog", ONTAPSECURITYAUDITLOG_MAPPING)
