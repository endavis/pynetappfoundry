"""OntapS3Audit type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.audit.object_store.model import OntapS3Audit

ONTAPS3AUDIT_MAPPING = TypeMapping(
    name="OntapS3Audit",
    model_class=OntapS3Audit,
    api_endpoint="/protocols/audit/{svm.uuid}/object-store?fields=*",
    api_type="ontap",
    parent_mapping="OntapAudit",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.data",
            api_path="events.data",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.management",
            api_path="events.management",
            default=False,
        ),
        FieldMapping(
            cache_attr="log.format",
            api_path="log.format",
        ),
        FieldMapping(
            cache_attr="log.retention.count",
            api_path="log.retention.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="log.retention.duration",
            api_path="log.retention.duration",
        ),
        FieldMapping(
            cache_attr="log.rotation.now",
            api_path="log.rotation.now",
            default=False,
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.days",
            api_path="log.rotation.schedule.days",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.hours",
            api_path="log.rotation.schedule.hours",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.minutes",
            api_path="log.rotation.schedule.minutes",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.months",
            api_path="log.rotation.schedule.months",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.schedule.weekdays",
            api_path="log.rotation.schedule.weekdays",
            default=[],
        ),
        FieldMapping(
            cache_attr="log.rotation.size",
            api_path="log.rotation.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_path",
            api_path="log_path",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3Audit", ONTAPS3AUDIT_MAPPING)
