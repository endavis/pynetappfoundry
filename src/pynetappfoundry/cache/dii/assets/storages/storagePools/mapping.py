"""DiiAssetsStoragesStoragepool type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.storagePools.model import (
    DiiAssetsStoragesStoragepool,
)

DIIASSETSSTORAGESSTORAGEPOOL_MAPPING = TypeMapping(
    name="DiiAssetsStoragesStoragepool",
    model_class=DiiAssetsStoragesStoragepool,
    api_endpoint="/assets/storages/{id}/storagePools",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsStorage",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="usesFlashPools",
            default=False,
        ),
        FieldMapping(
            cache_attr="internalVolumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="disks",
            default=[],
        ),
        FieldMapping(
            cache_attr="minDiskType",
        ),
        FieldMapping(
            cache_attr="vendorTier",
        ),
        FieldMapping(
            cache_attr="storageResources",
            default=[],
        ),
        FieldMapping(
            cache_attr="volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="isAutoTiering",
            default=False,
        ),
        FieldMapping(
            cache_attr="minDiskSpeed",
            default=0,
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
            cache_attr="capacity",
        ),
        FieldMapping(
            cache_attr="isRaidGroup",
            default=False,
        ),
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="datasources",
            default=[],
        ),
        FieldMapping(
            cache_attr="storageVirtualMachines",
            default=[],
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="storageNodes",
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="redundancy",
        ),
        FieldMapping(
            cache_attr="isVirtual",
            default=False,
        ),
        FieldMapping(
            cache_attr="minDiskSize",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsStoragesStoragepool", DIIASSETSSTORAGESSTORAGEPOOL_MAPPING
)
