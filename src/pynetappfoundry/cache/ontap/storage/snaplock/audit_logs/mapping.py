"""OntapSnaplockLog type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.audit_logs.model import (
    OntapSnaplockLog,
    OntapSnaplockLogLogFile,
)

ONTAPSNAPLOCKLOG_MAPPING = TypeMapping(
    name="OntapSnaplockLog",
    model_class=OntapSnaplockLog,
    api_endpoint="/storage/snaplock/audit-logs?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="log_archive.archive",
            default=False,
        ),
        FieldMapping(
            cache_attr="log_archive.base_name",
        ),
        FieldMapping(
            cache_attr="log_files",
            item_model=OntapSnaplockLogLogFile,
            default=[],
        ),
        FieldMapping(
            cache_attr="log_volume.max_log_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_volume.retention_period",
        ),
        FieldMapping(
            cache_attr="log_volume.volume.name",
        ),
        FieldMapping(
            cache_attr="log_volume.volume.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnaplockLog", ONTAPSNAPLOCKLOG_MAPPING)
