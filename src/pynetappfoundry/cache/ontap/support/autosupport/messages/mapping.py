"""OntapAutosupportMessage type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.autosupport.messages.model import OntapAutosupportMessage

ONTAPAUTOSUPPORTMESSAGE_MAPPING = TypeMapping(
    name="OntapAutosupportMessage",
    model_class=OntapAutosupportMessage,
    api_endpoint="/support/autosupport/messages?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="destination",
        ),
        FieldMapping(
            cache_attr="error.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="error.message",
        ),
        FieldMapping(
            cache_attr="generated_on",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="message",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="subject",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uri",
        ),
    ),
)

model_registry.register_mapping("OntapAutosupportMessage", ONTAPAUTOSUPPORTMESSAGE_MAPPING)
