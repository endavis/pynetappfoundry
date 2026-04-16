"""DiiAssetsFabricsCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.fabrics.count.model import DiiAssetsFabricsCount

DIIASSETSFABRICSCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsFabricsCount",
    model_class=DiiAssetsFabricsCount,
    api_endpoint="/assets/fabrics/count",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsFabricsCount", DIIASSETSFABRICSCOUNT_MAPPING)
