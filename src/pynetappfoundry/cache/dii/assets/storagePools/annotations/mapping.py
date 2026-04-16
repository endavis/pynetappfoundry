"""DiiAssetsStoragepoolsAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storagePools.annotations.model import (
    DiiAssetsStoragepoolsAnnotation,
)

DIIASSETSSTORAGEPOOLSANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsStoragepoolsAnnotation",
    model_class=DiiAssetsStoragepoolsAnnotation,
    api_endpoint="/assets/storagePools/{id}/annotations",
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
    "DiiAssetsStoragepoolsAnnotation", DIIASSETSSTORAGEPOOLSANNOTATION_MAPPING
)
