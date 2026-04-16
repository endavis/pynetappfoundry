"""DiiAssetsStoragesDisk type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.disks.model import DiiAssetsStoragesDisk

DIIASSETSSTORAGESDISK_MAPPING = TypeMapping(
    name="DiiAssetsStoragesDisk",
    model_class=DiiAssetsStoragesDisk,
    api_endpoint="/assets/storages/{id}/disks",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsStorage",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="role",
        ),
        FieldMapping(
            cache_attr="serialNumber",
        ),
        FieldMapping(
            cache_attr="storageResources",
            default=[],
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="storage",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="speed",
        ),
        FieldMapping(
            cache_attr="diskSize",
        ),
        FieldMapping(
            cache_attr="backendVolumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="storagePools",
            default=[],
        ),
        FieldMapping(
            cache_attr="datasources",
            default=[],
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="diskGroup",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="isVirtual",
            default=False,
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsStoragesDisk", DIIASSETSSTORAGESDISK_MAPPING)
