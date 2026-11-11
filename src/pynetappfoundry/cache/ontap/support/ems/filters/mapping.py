"""OntapEmsFilter type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.ems.filters.model import (
    OntapEmsFilter,
    OntapEmsFilterRule,
)

ONTAPEMSFILTER_MAPPING = TypeMapping(
    name="OntapEmsFilter",
    model_class=OntapEmsFilter,
    api_endpoint="/support/ems/filters?fields=*",
    api_type="ontap",
    identifier_field="name",
    fields=(
        FieldMapping(
            cache_attr="access_control_role.name",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="rules",
            item_model=OntapEmsFilterRule,
            default=[],
        ),
        FieldMapping(
            cache_attr="system_defined",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapEmsFilter", ONTAPEMSFILTER_MAPPING)
