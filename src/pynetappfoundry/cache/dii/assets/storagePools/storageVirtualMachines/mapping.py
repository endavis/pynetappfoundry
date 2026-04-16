"""DiiAssetsStoragepoolsStoragevirtualmachine type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storagePools.storageVirtualMachines.model import (
    DiiAssetsStoragepoolsStoragevirtualmachine,
)

DIIASSETSSTORAGEPOOLSSTORAGEVIRTUALMACHINE_MAPPING = TypeMapping(
    name="DiiAssetsStoragepoolsStoragevirtualmachine",
    model_class=DiiAssetsStoragepoolsStoragevirtualmachine,
    api_endpoint="/assets/storagePools/{id}/storageVirtualMachines",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="internalVolumeLimit",
            default=0,
        ),
        FieldMapping(
            cache_attr="internalVolumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="guidKey",
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
            cache_attr="ipSpace",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
        FieldMapping(
            cache_attr="qtrees",
            default=[],
        ),
        FieldMapping(
            cache_attr="shares",
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
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="protocols",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsStoragepoolsStoragevirtualmachine", DIIASSETSSTORAGEPOOLSSTORAGEVIRTUALMACHINE_MAPPING
)
