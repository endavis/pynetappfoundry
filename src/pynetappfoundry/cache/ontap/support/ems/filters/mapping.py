"""OntapEmsFilter type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.ems.filters.model import (
    OntapEmsFilter,
    OntapEmsFilterParameterCriteria,
)


def _transform_parameter_criteria(record: dict[str, Any]) -> list[OntapEmsFilterParameterCriteria]:
    """Transform parameter_criteria into OntapEmsFilterParameterCriteria list."""
    return [
        OntapEmsFilterParameterCriteria(**item) for item in record.get("parameter_criteria", [])
    ]


ONTAPEMSFILTER_MAPPING = TypeMapping(
    name="OntapEmsFilter",
    model_class=OntapEmsFilter,
    api_endpoint="/support/ems/filters/{name}?fields=*",
    api_type="ontap",
    records_path="rules",
    parent_mapping=None,
    parent_id_field=None,
    fields=(
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="message_criteria.name_pattern",
            api_path="message_criteria.name_pattern",
        ),
        FieldMapping(
            cache_attr="message_criteria.severities",
            api_path="message_criteria.severities",
        ),
        FieldMapping(
            cache_attr="message_criteria.snmp_trap_types",
            api_path="message_criteria.snmp_trap_types",
        ),
        FieldMapping(
            cache_attr="parameter_criteria",
            api_path="parameter_criteria",
            transform=_transform_parameter_criteria,
            default=[],
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapEmsFilter", ONTAPEMSFILTER_MAPPING)
