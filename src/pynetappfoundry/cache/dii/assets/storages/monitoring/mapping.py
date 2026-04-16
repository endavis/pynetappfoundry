"""DiiAssetsStoragesMonitoring type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.monitoring.model import DiiAssetsStoragesMonitoring

DIIASSETSSTORAGESMONITORING_MAPPING = TypeMapping(
    name="DiiAssetsStoragesMonitoring",
    model_class=DiiAssetsStoragesMonitoring,
    api_endpoint="/assets/storages/{id}/monitoring",
    api_type="dii",
    parent_mapping="DiiAssetsStorage",
    parent_id_field="id",
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

model_registry.register_mapping("DiiAssetsStoragesMonitoring", DIIASSETSSTORAGESMONITORING_MAPPING)
