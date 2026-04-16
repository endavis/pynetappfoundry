"""DiiAssetsStoragenodesMonitoring type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storageNodes.monitoring.model import (
    DiiAssetsStoragenodesMonitoring,
)

DIIASSETSSTORAGENODESMONITORING_MAPPING = TypeMapping(
    name="DiiAssetsStoragenodesMonitoring",
    model_class=DiiAssetsStoragenodesMonitoring,
    api_endpoint="/assets/storageNodes/{id}/monitoring",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="count",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsStoragenodesMonitoring", DIIASSETSSTORAGENODESMONITORING_MAPPING
)
