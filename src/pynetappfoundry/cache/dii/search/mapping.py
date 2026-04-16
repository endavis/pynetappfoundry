"""DiiSearchresultsummary type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.search.model import DiiSearchresultsummary

DIISEARCHRESULTSUMMARY_MAPPING = TypeMapping(
    name="DiiSearchresultsummary",
    model_class=DiiSearchresultsummary,
    api_endpoint="/search",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="searchString",
        ),
        FieldMapping(
            cache_attr="foundResults",
            default=False,
        ),
        FieldMapping(
            cache_attr="topHit",
        ),
        FieldMapping(
            cache_attr="resultsByCategory",
        ),
    ),
)

model_registry.register_mapping("DiiSearchresultsummary", DIISEARCHRESULTSUMMARY_MAPPING)
