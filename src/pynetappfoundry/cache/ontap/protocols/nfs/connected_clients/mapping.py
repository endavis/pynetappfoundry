"""OntapNfsClients type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.connected_clients.model import OntapNfsClients

ONTAPNFSCLIENTS_MAPPING = TypeMapping(
    name="OntapNfsClients",
    model_class=OntapNfsClients,
    api_endpoint="/protocols/nfs/connected-clients?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_ip",
        ),
        FieldMapping(
            cache_attr="export_policy.id",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="export_policy.name",
        ),
        FieldMapping(
            cache_attr="idle_duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="local_request_count",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="remote_request_count",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="server_ip",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="trunking_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNfsClients", ONTAPNFSCLIENTS_MAPPING)
