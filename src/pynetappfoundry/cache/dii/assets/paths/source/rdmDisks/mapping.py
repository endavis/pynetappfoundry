"""DiiAssetsPathsSourceRdmdisk type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.source.rdmDisks.model import (
    DiiAssetsPathsSourceRdmdisk,
)

DIIASSETSPATHSSOURCERDMDISK_MAPPING = TypeMapping(
    name="DiiAssetsPathsSourceRdmdisk",
    model_class=DiiAssetsPathsSourceRdmdisk,
    api_endpoint="/assets/paths/{id}/source/rdmDisks",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="virtualMachine",
        ),
        FieldMapping(
            cache_attr="performance",
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
            cache_attr="storageResources",
            default=[],
        ),
        FieldMapping(
            cache_attr="dataStore",
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
            cache_attr="isRdm",
            default=False,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsPathsSourceRdmdisk", DIIASSETSPATHSSOURCERDMDISK_MAPPING)
