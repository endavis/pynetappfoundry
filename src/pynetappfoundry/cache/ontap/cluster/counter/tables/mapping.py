"""OntapCounterTable type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.counter.tables.model import (
    OntapCounterTable,
    OntapCounterTableCounterSchema,
)

ONTAPCOUNTERTABLE_MAPPING = TypeMapping(
    name="OntapCounterTable",
    model_class=OntapCounterTable,
    api_endpoint="/cluster/counter/tables?fields=*",
    api_type="ontap",
    identifier_field="name",
    fields=(
        FieldMapping(
            cache_attr="counter_schemas",
            item_model=OntapCounterTableCounterSchema,
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
