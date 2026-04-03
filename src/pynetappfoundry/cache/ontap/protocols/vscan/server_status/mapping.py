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
            cache_attr="ip",
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
            cache_attr="update_time",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping("OntapVscanServerStatus", ONTAPVSCANSERVERSTATUS_MAPPING)
