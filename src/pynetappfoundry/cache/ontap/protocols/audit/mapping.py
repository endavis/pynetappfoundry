"""OntapAudit type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.audit.model import OntapAudit

ONTAPAUDIT_MAPPING = TypeMapping(
    name="OntapAudit",
    model_class=OntapAudit,
    api_endpoint="/protocols/audit?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="charge_qos",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.async_delete",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.audit_policy_change",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.authorization_policy",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.cap_staging",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.cifs_logon_logoff",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.file_operations",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.file_share",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.security_group",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.user_account",
            default=False,
        ),
        FieldMapping(
            cache_attr="guarantee",
            default=False,
        ),
        FieldMapping(
            cache_attr="log.format",
        ),
        FieldMapping(
            cache_attr="log.retention.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="log.retention.duration",
        ),
        FieldMapping(
            cache_attr="log.rotation.now",
            default=False,
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.days",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.hours",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.minutes",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.months",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.weekdays",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_path",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapAudit", ONTAPAUDIT_MAPPING)
