"""OntapFpolicyConnection type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.fpolicy.connections.model import OntapFpolicyConnection

ONTAPFPOLICYCONNECTION_MAPPING = TypeMapping(
    name="OntapFpolicyConnection",
    model_class=OntapFpolicyConnection,
    api_endpoint="/protocols/fpolicy/{svm.uuid}/connections?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="disconnected_reason.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="disconnected_reason.message",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="policy.name",
        ),
        FieldMapping(
            cache_attr="server",
        ),
        FieldMapping(
            cache_attr="session_uuid",
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
    ),
)

model_registry.register_mapping("OntapFpolicyConnection", ONTAPFPOLICYCONNECTION_MAPPING)
