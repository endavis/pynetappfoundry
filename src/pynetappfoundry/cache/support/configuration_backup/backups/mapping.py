"""OntapConfigurationBackupFile type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.support.configuration_backup.backups.model import (
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
            api_path="auto",
            default=False,
        ),
        FieldMapping(
            cache_attr="backup_nodes",
            transform=_transform_backup_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="download_link",
            api_path="download_link",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
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
            cache_attr="size",
            api_path="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="time",
            api_path="time",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping(
    "OntapConfigurationBackupFile", ONTAPCONFIGURATIONBACKUPFILE_MAPPING
)
