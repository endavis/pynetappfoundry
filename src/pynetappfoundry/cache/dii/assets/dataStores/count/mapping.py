"""DiiAssetsDatastoresCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.dataStores.count.model import DiiAssetsDatastoresCount

DIIASSETSDATASTORESCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsDatastoresCount",
    model_class=DiiAssetsDatastoresCount,
    api_endpoint="/assets/dataStores/count",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsDatastoresCount", DIIASSETSDATASTORESCOUNT_MAPPING)
