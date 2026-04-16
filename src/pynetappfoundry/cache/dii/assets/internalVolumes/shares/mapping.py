"""DiiAssetsInternalvolumesShare type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.internalVolumes.shares.model import (
    DiiAssetsInternalvolumesShare,
)

DIIASSETSINTERNALVOLUMESSHARE_MAPPING = TypeMapping(
    name="DiiAssetsInternalvolumesShare",
    model_class=DiiAssetsInternalvolumesShare,
    api_endpoint="/assets/internalVolumes/{id}/shares",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="qtree",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="storage",
        ),
        FieldMapping(
            cache_attr="internalVolume",
        ),
        FieldMapping(
            cache_attr="initiators",
            default=[],
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="storageVirtualMachine",
        ),
        FieldMapping(
            cache_attr="datasources",
            default=[],
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="storagePool",
        ),
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsInternalvolumesShare", DIIASSETSINTERNALVOLUMESSHARE_MAPPING
)
