"""DiiAssetsStoragesRisk type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.risks.model import DiiAssetsStoragesRisk

DIIASSETSSTORAGESRISK_MAPPING = TypeMapping(
    name="DiiAssetsStoragesRisk",
    model_class=DiiAssetsStoragesRisk,
    api_endpoint="/assets/storages/{id}/risks",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsStorage",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="severity",
        ),
        FieldMapping(
            cache_attr="sourceId",
            default=0,
        ),
        FieldMapping(
            cache_attr="parent",
        ),
        FieldMapping(
            cache_attr="resource",
        ),
        FieldMapping(
            cache_attr="impact",
        ),
        FieldMapping(
            cache_attr="link",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="sourceType",
        ),
        FieldMapping(
            cache_attr="mitigationCategory",
        ),
        FieldMapping(
            cache_attr="riskSource",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="details",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="category",
        ),
        FieldMapping(
            cache_attr="statusCode",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsStoragesRisk", DIIASSETSSTORAGESRISK_MAPPING)
