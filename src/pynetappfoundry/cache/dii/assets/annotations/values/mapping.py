"""DiiAssetsAnnotationsValue type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.annotations.values.model import DiiAssetsAnnotationsValue

DIIASSETSANNOTATIONSVALUE_MAPPING = TypeMapping(
    name="DiiAssetsAnnotationsValue",
    model_class=DiiAssetsAnnotationsValue,
    api_endpoint="/assets/annotations/{id}/values",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsAnnotation",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="values",
            default=[],
        ),
        FieldMapping(
            cache_attr="objectType",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsAnnotationsValue", DIIASSETSANNOTATIONSVALUE_MAPPING)
