"""DiiAssetsInternalvolumesAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.internalVolumes.annotations.model import (
    DiiAssetsInternalvolumesAnnotation,
)

DIIASSETSINTERNALVOLUMESANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsInternalvolumesAnnotation",
    model_class=DiiAssetsInternalvolumesAnnotation,
    api_endpoint="/assets/internalVolumes/{id}/annotations",
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

model_registry.register_mapping(
    "DiiAssetsInternalvolumesAnnotation", DIIASSETSINTERNALVOLUMESANNOTATION_MAPPING
)
