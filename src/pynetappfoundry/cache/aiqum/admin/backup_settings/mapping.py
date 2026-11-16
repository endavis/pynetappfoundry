"""AiqumBackupSettings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.admin.backup_settings.model import AiqumBackupSettings

AIQUMBACKUPSETTINGS_MAPPING = TypeMapping(
    name="AiqumBackupSettings",
    model_class=AiqumBackupSettings,
    api_endpoint="/admin/backup-settings",
    api_type="aiqum",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="day_of_week",
        ),
        FieldMapping(
            cache_attr="frequency",
        ),
        FieldMapping(
            cache_attr="hour",
            default=0,
        ),
        FieldMapping(
            cache_attr="minute",
            default=0,
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="retention_count",
            default=0,
        ),
    ),
)

model_registry.register_mapping("AiqumBackupSettings", AIQUMBACKUPSETTINGS_MAPPING)
