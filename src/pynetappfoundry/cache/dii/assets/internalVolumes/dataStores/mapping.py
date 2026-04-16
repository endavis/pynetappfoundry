"""DiiAssetsInternalvolumesDatastore type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.internalVolumes.dataStores.model import (
    DiiAssetsInternalvolumesDatastore,
)

DIIASSETSINTERNALVOLUMESDATASTORE_MAPPING = TypeMapping(
    name="DiiAssetsInternalvolumesDatastore",
    model_class=DiiAssetsInternalvolumesDatastore,
    api_endpoint="/assets/internalVolumes/{id}/dataStores",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="virtualCenterIp",
        ),
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="vmdks",
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
            cache_attr="hosts",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
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
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="virtualMachines",
            default=[],
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsInternalvolumesDatastore", DIIASSETSINTERNALVOLUMESDATASTORE_MAPPING
)
