"""OntapConfigurationBackupFile type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.configuration_backup.backups.model import (
    OntapConfigurationBackupFile,
    OntapConfigurationBackupFileBackupNode,
)


def _transform_backup_nodes(record: dict[str, Any]) -> list[OntapConfigurationBackupFileBackupNode]:
    """Transform backup_nodes into OntapConfigurationBackupFileBackupNode list."""
    return [
        OntapConfigurationBackupFileBackupNode(**item) for item in record.get("backup_nodes", [])
    ]


ONTAPCONFIGURATIONBACKUPFILE_MAPPING = TypeMapping(
    name="OntapConfigurationBackupFile",
    model_class=OntapConfigurationBackupFile,
    api_endpoint="/support/configuration-backup/backups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="auto",
            default=False,
        ),
        FieldMapping(
            cache_attr="backup_nodes",
            transform=_transform_backup_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="download_link",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="time",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping(
    "OntapConfigurationBackupFile", ONTAPCONFIGURATIONBACKUPFILE_MAPPING
)
