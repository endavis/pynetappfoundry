"""DiiAssetsStoragenodesAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storageNodes.annotations.model import (
    DiiAssetsStoragenodesAnnotation,
)

DIIASSETSSTORAGENODESANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsStoragenodesAnnotation",
    model_class=DiiAssetsStoragenodesAnnotation,
    api_endpoint="/assets/storageNodes/{id}/annotations",
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
    "DiiAssetsStoragenodesAnnotation", DIIASSETSSTORAGENODESANNOTATION_MAPPING
)
