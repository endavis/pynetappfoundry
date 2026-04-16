"""DiiAssetsHostsCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.hosts.count.model import DiiAssetsHostsCount

DIIASSETSHOSTSCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsHostsCount",
    model_class=DiiAssetsHostsCount,
    api_endpoint="/assets/hosts/count",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsHostsCount", DIIASSETSHOSTSCOUNT_MAPPING)
