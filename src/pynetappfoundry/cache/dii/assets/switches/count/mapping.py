"""DiiAssetsSwitchesCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.switches.count.model import DiiAssetsSwitchesCount

DIIASSETSSWITCHESCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsSwitchesCount",
    model_class=DiiAssetsSwitchesCount,
    api_endpoint="/assets/switches/count",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsSwitchesCount", DIIASSETSSWITCHESCOUNT_MAPPING)
