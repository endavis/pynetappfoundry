"""OntapEmsEventResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.ems.events.model import (
    OntapEmsEventResponse,
    OntapEmsEventResponseParameter,
)


def _transform_parameters(record: dict[str, Any]) -> list[OntapEmsEventResponseParameter]:
    """Transform parameters into OntapEmsEventResponseParameter list."""
    return [OntapEmsEventResponseParameter(**item) for item in record.get("parameters", [])]


ONTAPEMSEVENTRESPONSE_MAPPING = TypeMapping(
    name="OntapEmsEventResponse",
    model_class=OntapEmsEventResponse,
    api_endpoint="/support/ems/events?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_message",
        ),
        FieldMapping(
            cache_attr="message.name",
        ),
        FieldMapping(
            cache_attr="message.severity",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="parameters",
            transform=_transform_parameters,
            default=[],
        ),
        FieldMapping(
            cache_attr="source",
        ),
        FieldMapping(
            cache_attr="time",
        ),
    ),
)

model_registry.register_mapping("OntapEmsEventResponse", ONTAPEMSEVENTRESPONSE_MAPPING)
