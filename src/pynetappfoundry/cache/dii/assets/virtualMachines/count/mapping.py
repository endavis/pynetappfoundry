"""DiiAssetsVirtualmachinesCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.virtualMachines.count.model import (
    DiiAssetsVirtualmachinesCount,
)

DIIASSETSVIRTUALMACHINESCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsVirtualmachinesCount",
    model_class=DiiAssetsVirtualmachinesCount,
    api_endpoint="/assets/virtualMachines/count",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVirtualmachinesCount", DIIASSETSVIRTUALMACHINESCOUNT_MAPPING
)
