"""OntapSnaplockLog type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.snaplock.audit_logs.model import (
    OntapSnaplockLog,
    OntapSnaplockLogLogFile,
)


def _transform_log_files(record: dict[str, Any]) -> list[OntapSnaplockLogLogFile]:
    """Transform log_files into OntapSnaplockLogLogFile list."""
    return [OntapSnaplockLogLogFile(**item) for item in record.get("log_files", [])]


ONTAPSNAPLOCKLOG_MAPPING = TypeMapping(
    name="OntapSnaplockLog",
    model_class=OntapSnaplockLog,
    api_endpoint="/storage/snaplock/audit-logs?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="log_archive_archive",
            api_path="log_archive.archive",
            default=False,
        ),
        FieldMapping(
            cache_attr="log_archive_base_name",
            api_path="log_archive.base_name",
        ),
        FieldMapping(
            cache_attr="log_files",
            transform=_transform_log_files,
            default=[],
        ),
        FieldMapping(
            cache_attr="log_volume_max_log_size",
            api_path="log_volume.max_log_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_volume_retention_period",
            api_path="log_volume.retention_period",
        ),
        FieldMapping(
            cache_attr="log_volume_volume_name",
            api_path="log_volume.volume.name",
        ),
        FieldMapping(
            cache_attr="log_volume_volume_uuid",
            api_path="log_volume.volume.uuid",
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

model_registry.register_mapping("OntapSnaplockLog", ONTAPSNAPLOCKLOG_MAPPING)
