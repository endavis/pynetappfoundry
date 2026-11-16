"""AiqumBackupFileInfo type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.admin.backup_file_info.model import AiqumBackupFileInfo

AIQUMBACKUPFILEINFO_MAPPING = TypeMapping(
    name="AiqumBackupFileInfo",
    model_class=AiqumBackupFileInfo,
    api_endpoint="/admin/backup-file-info",
    api_type="aiqum",
    fields=(
        FieldMapping(
            cache_attr="creation_time",
        ),
        FieldMapping(
            cache_attr="is_scheduled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="size",
            default=0,
        ),
    ),
)

model_registry.register_mapping("AiqumBackupFileInfo", AIQUMBACKUPFILEINFO_MAPPING)
