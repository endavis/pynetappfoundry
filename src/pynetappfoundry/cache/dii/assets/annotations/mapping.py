"""DiiAssetsAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.annotations.model import DiiAssetsAnnotation

DIIASSETSANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsAnnotation",
    model_class=DiiAssetsAnnotation,
    api_endpoint="/assets/annotations",
    api_type="dii",
    identifier_field="id",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="isUserDefined",
            default=False,
        ),
        FieldMapping(
            cache_attr="isCostBased",
            default=False,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="label",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="supportedObjectTypes",
            default=[],
        ),
        FieldMapping(
            cache_attr="enumValues",
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiAssetsAnnotation", DIIASSETSANNOTATION_MAPPING)
