"""DiiQuery type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.queries.model import DiiQuery

DIIQUERY_MAPPING = TypeMapping(
    name="DiiQuery",
    model_class=DiiQuery,
    api_endpoint="/queries",
    api_type="dii",
    identifier_field="id",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="owner",
        ),
        FieldMapping(
            cache_attr="objectMeasurement",
        ),
        FieldMapping(
            cache_attr="expression",
        ),
        FieldMapping(
            cache_attr="schemaVersion",
            default=0,
        ),
        FieldMapping(
            cache_attr="offset",
            default=0,
        ),
        FieldMapping(
            cache_attr="sort",
        ),
        FieldMapping(
            cache_attr="groupBy",
            default=[],
        ),
        FieldMapping(
            cache_attr="creationDate",
        ),
        FieldMapping(
            cache_attr="ownerid",
        ),
        FieldMapping(
            cache_attr="objectType",
        ),
        FieldMapping(
            cache_attr="otherProps",
        ),
        FieldMapping(
            cache_attr="stickyPaneWidth",
            default=0,
        ),
        FieldMapping(
            cache_attr="groupByFieldWidths",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="limit",
            default=0,
        ),
        FieldMapping(
            cache_attr="fromTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="fields",
            default=[],
        ),
        FieldMapping(
            cache_attr="toTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="objectCategory",
        ),
        FieldMapping(
            cache_attr="timeRange",
        ),
    ),
)

model_registry.register_mapping("DiiQuery", DIIQUERY_MAPPING)
