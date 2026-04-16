"""OntapVscanEvent type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.events.model import OntapVscanEvent

ONTAPVSCANEVENT_MAPPING = TypeMapping(
    name="OntapVscanEvent",
    model_class=OntapVscanEvent,
    api_endpoint="/protocols/vscan/{svm.uuid}/events?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="disconnect_reason",
        ),
        FieldMapping(
            cache_attr="event_time",
        ),
        FieldMapping(
            cache_attr="file_path",
        ),
        FieldMapping(
            cache_attr="interface.ip.address",
        ),
        FieldMapping(
            cache_attr="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="server",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping("OntapVscanEvent", ONTAPVSCANEVENT_MAPPING)
