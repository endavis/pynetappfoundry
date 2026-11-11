"""OntapCounterRow type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.counter.tables.rows.model import (
    OntapCounterRow,
    OntapCounterRowCounter,
    OntapCounterRowProperty,
)

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
            item_model=OntapCounterRowCounter,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="properties",
            item_model=OntapCounterRowProperty,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapCounterRow", ONTAPCOUNTERROW_MAPPING)
