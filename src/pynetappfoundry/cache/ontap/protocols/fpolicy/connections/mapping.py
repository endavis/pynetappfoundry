"""OntapFpolicyConnection type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.fpolicy.connections.model import OntapFpolicyConnection

ONTAPFPOLICYCONNECTION_MAPPING = TypeMapping(
    name="OntapFpolicyConnection",
    model_class=OntapFpolicyConnection,
    api_endpoint="/protocols/fpolicy/{svm.uuid}/connections?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="disconnected_reason_code",
            api_path="disconnected_reason.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="disconnected_reason_message",
            api_path="disconnected_reason.message",
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
            cache_attr="policy_name",
            api_path="policy.name",
        ),
        FieldMapping(
            cache_attr="server",
            api_path="server",
        ),
        FieldMapping(
            cache_attr="session_uuid",
            api_path="session_uuid",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
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
            cache_attr="update_time",
            api_path="update_time",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicyConnection", ONTAPFPOLICYCONNECTION_MAPPING)
