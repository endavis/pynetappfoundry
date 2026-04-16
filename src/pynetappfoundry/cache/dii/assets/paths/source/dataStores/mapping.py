"""DiiAssetsPathsSourceDatastore type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.source.dataStores.model import (
    DiiAssetsPathsSourceDatastore,
)

DIIASSETSPATHSSOURCEDATASTORE_MAPPING = TypeMapping(
    name="DiiAssetsPathsSourceDatastore",
    model_class=DiiAssetsPathsSourceDatastore,
    api_endpoint="/assets/paths/{id}/source/dataStores",
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
    "DiiAssetsPathsSourceDatastore", DIIASSETSPATHSSOURCEDATASTORE_MAPPING
)
