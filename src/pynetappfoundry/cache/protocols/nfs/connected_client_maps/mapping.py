"""OntapNfsClientsMap type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.nfs.connected_client_maps.model import OntapNfsClientsMap

ONTAPNFSCLIENTSMAP_MAPPING = TypeMapping(
    name="OntapNfsClientsMap",
    model_class=OntapNfsClientsMap,
    api_endpoint="/protocols/nfs/connected-client-maps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_ips",
            api_path="client_ips",
            default=[],
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
    ),
)

model_registry.register_mapping("OntapNfsClientsMap", ONTAPNFSCLIENTSMAP_MAPPING)
