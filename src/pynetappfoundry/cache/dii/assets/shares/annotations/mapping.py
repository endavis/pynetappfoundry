"""DiiAssetsSharesAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.shares.annotations.model import DiiAssetsSharesAnnotation

DIIASSETSSHARESANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsSharesAnnotation",
    model_class=DiiAssetsSharesAnnotation,
    api_endpoint="/assets/shares/{id}/annotations",
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

model_registry.register_mapping("DiiAssetsSharesAnnotation", DIIASSETSSHARESANNOTATION_MAPPING)
