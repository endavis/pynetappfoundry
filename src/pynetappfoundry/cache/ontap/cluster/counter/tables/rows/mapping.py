"""OntapCounterRow type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.counter.tables.rows.model import (
    OntapCounterRow,
    OntapCounterRowCounter,
    OntapCounterRowProperty,
)


def _transform_counters(record: dict[str, Any]) -> list[OntapCounterRowCounter]:
    """Transform counters into OntapCounterRowCounter list."""
    return [OntapCounterRowCounter(**item) for item in record.get("counters", [])]


def _transform_properties(record: dict[str, Any]) -> list[OntapCounterRowProperty]:
    """Transform properties into OntapCounterRowProperty list."""
    return [OntapCounterRowProperty(**item) for item in record.get("properties", [])]


ONTAPCOUNTERROW_MAPPING = TypeMapping(
    name="OntapCounterRow",
    model_class=OntapCounterRow,
    api_endpoint="/cluster/counter/tables/{counter_table.name}/rows?fields=*",
    api_type="ontap",
    parent_mapping="OntapCounterTable",
    parent_id_field="name",
    fields=(
        FieldMapping(
            cache_attr="aggregation.complete",
            default=False,
        ),
        FieldMapping(
            cache_attr="aggregation.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="counter_table.name",
        ),
        FieldMapping(
            cache_attr="counters",
            transform=_transform_counters,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="properties",
            transform=_transform_properties,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapCounterRow", ONTAPCOUNTERROW_MAPPING)
