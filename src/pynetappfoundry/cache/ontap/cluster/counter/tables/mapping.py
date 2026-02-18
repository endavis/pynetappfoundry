"""OntapCounterTable type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.counter.tables.model import OntapCounterTable

ONTAPCOUNTERTABLE_MAPPING = TypeMapping(
    name="OntapCounterTable",
    model_class=OntapCounterTable,
    api_endpoint="/cluster/counter/tables/{name}?fields=*",
    api_type="ontap",
    records_path="counter_schemas",
    parent_mapping="OntapClusterCounterTable",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="denominator_name",
            api_path="denominator.name",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="unit",
            api_path="unit",
        ),
    ),
)

model_registry.register_mapping("OntapCounterTable", ONTAPCOUNTERTABLE_MAPPING)
