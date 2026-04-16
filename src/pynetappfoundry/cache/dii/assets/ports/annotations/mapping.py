"""DiiAssetsPortsAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.ports.annotations.model import DiiAssetsPortsAnnotation

DIIASSETSPORTSANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsPortsAnnotation",
    model_class=DiiAssetsPortsAnnotation,
    api_endpoint="/assets/ports/{id}/annotations",
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

model_registry.register_mapping("DiiAssetsPortsAnnotation", DIIASSETSPORTSANNOTATION_MAPPING)
