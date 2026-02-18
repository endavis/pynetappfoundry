"""OntapAutosupportMessage type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.autosupport.messages.model import OntapAutosupportMessage

ONTAPAUTOSUPPORTMESSAGE_MAPPING = TypeMapping(
    name="OntapAutosupportMessage",
    model_class=OntapAutosupportMessage,
    api_endpoint="/support/autosupport/messages?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="destination",
            api_path="destination",
        ),
        FieldMapping(
            cache_attr="error_code",
            api_path="error.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="error_message",
            api_path="error.message",
        ),
        FieldMapping(
            cache_attr="generated_on",
            api_path="generated_on",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="message",
            api_path="message",
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
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="subject",
            api_path="subject",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uri",
            api_path="uri",
        ),
    ),
)

model_registry.register_mapping("OntapAutosupportMessage", ONTAPAUTOSUPPORTMESSAGE_MAPPING)
