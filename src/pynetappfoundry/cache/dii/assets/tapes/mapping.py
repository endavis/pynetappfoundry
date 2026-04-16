"""DiiAssetsTape type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.tapes.model import DiiAssetsTape

DIIASSETSTAPE_MAPPING = TypeMapping(
    name="DiiAssetsTape",
    model_class=DiiAssetsTape,
    api_endpoint="/assets/tapes/{id}",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="serialNumber",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="fcPortCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="isActive",
            default=False,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsTape", DIIASSETSTAPE_MAPPING)
