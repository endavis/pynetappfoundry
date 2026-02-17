"""OntapNfsClients type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.nfs.connected_clients.model import OntapNfsClients

ONTAPNFSCLIENTS_MAPPING = TypeMapping(
    name="OntapNfsClients",
    model_class=OntapNfsClients,
    api_endpoint="/protocols/nfs/connected-clients?fields=*,export_policy",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_ip",
            api_path="client_ip",
        ),
        FieldMapping(
            cache_attr="export_policy_id",
            api_path="export_policy.id",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="export_policy_name",
            api_path="export_policy.name",
        ),
        FieldMapping(
            cache_attr="idle_duration",
            api_path="idle_duration",
        ),
        FieldMapping(
            cache_attr="local_request_count",
            api_path="local_request_count",
            default=0,
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
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="remote_request_count",
            api_path="remote_request_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="server_ip",
            api_path="server_ip",
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
            cache_attr="trunking_enabled",
            api_path="trunking_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNfsClients", ONTAPNFSCLIENTS_MAPPING)
