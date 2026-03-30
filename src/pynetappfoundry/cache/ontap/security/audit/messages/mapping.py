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
            api_path="application",
        ),
        FieldMapping(
            cache_attr="command_id",
            api_path="command_id",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="input",
            api_path="input",
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="message",
            api_path="message",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="session_id",
            api_path="session_id",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="timestamp",
            api_path="timestamp",
        ),
        FieldMapping(
            cache_attr="user",
            api_path="user",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityAuditLog", ONTAPSECURITYAUDITLOG_MAPPING)
