"""DiiAssetsVmdksAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.vmdks.annotations.model import DiiAssetsVmdksAnnotation

DIIASSETSVMDKSANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsVmdksAnnotation",
    model_class=DiiAssetsVmdksAnnotation,
    api_endpoint="/assets/vmdks/{id}/annotations",
    api_type="dii",
    records_path="",
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

model_registry.register_mapping("DiiAssetsVmdksAnnotation", DIIASSETSVMDKSANNOTATION_MAPPING)
