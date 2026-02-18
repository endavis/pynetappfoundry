"""OntapEmsEventResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.ems.events.model import (
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
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="log_message",
            api_path="log_message",
        ),
        FieldMapping(
            cache_attr="message_name",
            api_path="message.name",
        ),
        FieldMapping(
            cache_attr="message_severity",
            api_path="message.severity",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="parameters",
            transform=_transform_parameters,
            default=[],
        ),
        FieldMapping(
            cache_attr="source",
            api_path="source",
        ),
        FieldMapping(
            cache_attr="time",
            api_path="time",
        ),
    ),
)

model_registry.register_mapping("OntapEmsEventResponse", ONTAPEMSEVENTRESPONSE_MAPPING)
