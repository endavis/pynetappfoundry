"""OntapCounterTable type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.counter.tables.model import (
    OntapCounterTable,
    OntapCounterTableCounterSchema,
)


def _transform_counter_schemas(record: dict[str, Any]) -> list[OntapCounterTableCounterSchema]:
    """Transform counter_schemas into OntapCounterTableCounterSchema list."""
    return [OntapCounterTableCounterSchema(**item) for item in record.get("counter_schemas", [])]


ONTAPCOUNTERTABLE_MAPPING = TypeMapping(
    name="OntapCounterTable",
    model_class=OntapCounterTable,
    api_endpoint="/cluster/counter/tables?fields=*",
    api_type="ontap",
    identifier_field="name",
    fields=(
        FieldMapping(
            cache_attr="counter_schemas",
            transform=_transform_counter_schemas,
            default=[],
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="name",
        ),
    ),
)

model_registry.register_mapping("OntapCounterTable", ONTAPCOUNTERTABLE_MAPPING)
