"""OntapS3Audit type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.audit.object_store.model import OntapS3Audit

ONTAPS3AUDIT_MAPPING = TypeMapping(
    name="OntapS3Audit",
    model_class=OntapS3Audit,
    api_endpoint="/protocols/audit/{svm.uuid}/object-store?fields=*",
    api_type="ontap",
    parent_mapping="OntapAudit",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="events_data",
            api_path="events.data",
            default=False,
        ),
        FieldMapping(
            cache_attr="events_management",
            api_path="events.management",
            default=False,
        ),
        FieldMapping(
            cache_attr="log_format",
            api_path="log.format",
        ),
        FieldMapping(
            cache_attr="log_retention_count",
            api_path="log.retention.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_retention_duration",
            api_path="log.retention.duration",
        ),
        FieldMapping(
            cache_attr="log_rotation_now",
            api_path="log.rotation.now",
            default=False,
        ),
        FieldMapping(
            cache_attr="log_rotation_schedule_days",
            api_path="log.rotation.schedule.days",
            default=[],
        ),
        FieldMapping(
            cache_attr="log_rotation_schedule_hours",
            api_path="log.rotation.schedule.hours",
            default=[],
        ),
        FieldMapping(
            cache_attr="log_rotation_schedule_minutes",
            api_path="log.rotation.schedule.minutes",
            default=[],
        ),
        FieldMapping(
            cache_attr="log_rotation_schedule_months",
            api_path="log.rotation.schedule.months",
            default=[],
        ),
        FieldMapping(
            cache_attr="log_rotation_schedule_weekdays",
            api_path="log.rotation.schedule.weekdays",
            default=[],
        ),
        FieldMapping(
            cache_attr="log_rotation_size",
            api_path="log.rotation.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_path",
            api_path="log_path",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3Audit", ONTAPS3AUDIT_MAPPING)
