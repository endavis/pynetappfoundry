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
            default=False,
        ),
        FieldMapping(
            cache_attr="events.data",
            default=False,
        ),
        FieldMapping(
            cache_attr="events.management",
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

model_registry.register_mapping("OntapS3Audit", ONTAPS3AUDIT_MAPPING)
