"""DiiAssetsStoragesAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.annotations.model import DiiAssetsStoragesAnnotation

DIIASSETSSTORAGESANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsStoragesAnnotation",
    model_class=DiiAssetsStoragesAnnotation,
    api_endpoint="/assets/storages/{id}/annotations",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsStorage",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="displayValue",
        ),
        FieldMapping(
            cache_attr="rawValue",
        ),
        FieldMapping(
            cache_attr="definition",
        ),
        FieldMapping(
            cache_attr="label",
        ),
        FieldMapping(
            cache_attr="annotationAssignment",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsStoragesAnnotation", DIIASSETSSTORAGESANNOTATION_MAPPING)
