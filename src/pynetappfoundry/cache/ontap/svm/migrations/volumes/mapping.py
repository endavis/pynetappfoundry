"""OntapSvmMigrationVolume type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.migrations.volumes.model import (
    OntapSvmMigrationVolume,
    OntapSvmMigrationVolumeError,
)


def _transform_errors(record: dict[str, Any]) -> list[OntapSvmMigrationVolumeError]:
    """Transform errors into OntapSvmMigrationVolumeError list."""
    return [OntapSvmMigrationVolumeError(**item) for item in record.get("errors", [])]


ONTAPSVMMIGRATIONVOLUME_MAPPING = TypeMapping(
    name="OntapSvmMigrationVolume",
    model_class=OntapSvmMigrationVolume,
    api_endpoint="/svm/migrations/{svm_migration.uuid}/volumes?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvmMigration",
    parent_id_field="uuid",
    identifier_field="volume.uuid",
    fields=(
        FieldMapping(
            cache_attr="errors",
            transform=_transform_errors,
            default=[],
        ),
        FieldMapping(
            cache_attr="healthy",
            default=False,
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="transfer_state",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmMigrationVolume", ONTAPSVMMIGRATIONVOLUME_MAPPING)
