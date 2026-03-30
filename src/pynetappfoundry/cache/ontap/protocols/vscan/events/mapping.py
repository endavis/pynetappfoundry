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
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="disconnect_reason",
            api_path="disconnect_reason",
        ),
        FieldMapping(
            cache_attr="event_time",
            api_path="event_time",
        ),
        FieldMapping(
            cache_attr="file_path",
            api_path="file_path",
        ),
        FieldMapping(
            cache_attr="interface_ip_address",
            api_path="interface.ip.address",
        ),
        FieldMapping(
            cache_attr="interface_name",
            api_path="interface.name",
        ),
        FieldMapping(
            cache_attr="interface_uuid",
            api_path="interface.uuid",
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
            cache_attr="server",
            api_path="server",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="vendor",
            api_path="vendor",
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping("OntapVscanEvent", ONTAPVSCANEVENT_MAPPING)
