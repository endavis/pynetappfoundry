"""DiiAssetsQuotasAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.quotas.annotations.model import DiiAssetsQuotasAnnotation

DIIASSETSQUOTASANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsQuotasAnnotation",
    model_class=DiiAssetsQuotasAnnotation,
    api_endpoint="/assets/quotas/{id}/annotations",
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

model_registry.register_mapping("DiiAssetsQuotasAnnotation", DIIASSETSQUOTASANNOTATION_MAPPING)
