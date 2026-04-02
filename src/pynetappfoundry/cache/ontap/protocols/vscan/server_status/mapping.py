"""OntapVscanServerStatus type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.server_status.model import OntapVscanServerStatus

ONTAPVSCANSERVERSTATUS_MAPPING = TypeMapping(
    name="OntapVscanServerStatus",
    model_class=OntapVscanServerStatus,
    api_endpoint="/protocols/vscan/server-status?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="disconnected_reason",
            api_path="disconnected_reason",
        ),
        FieldMapping(
            cache_attr="interface.ip.address",
            api_path="interface.ip.address",
        ),
        FieldMapping(
            cache_attr="interface.name",
            api_path="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
            api_path="interface.uuid",
        ),
        FieldMapping(
            cache_attr="ip",
            api_path="ip",
        ),
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="update_time",
            api_path="update_time",
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

model_registry.register_mapping("OntapVscanServerStatus", ONTAPVSCANSERVERSTATUS_MAPPING)
