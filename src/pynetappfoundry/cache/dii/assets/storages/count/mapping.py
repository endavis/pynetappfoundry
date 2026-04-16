"""DiiAssetsStoragesCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.count.model import DiiAssetsStoragesCount

DIIASSETSSTORAGESCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsStoragesCount",
    model_class=DiiAssetsStoragesCount,
    api_endpoint="/assets/storages/count",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsStoragesCount", DIIASSETSSTORAGESCOUNT_MAPPING)
