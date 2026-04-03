"""OntapNfsClientsMap type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.connected_client_maps.model import (
    OntapNfsClientsMap,
)

ONTAPNFSCLIENTSMAP_MAPPING = TypeMapping(
    name="OntapNfsClientsMap",
    model_class=OntapNfsClientsMap,
    api_endpoint="/protocols/nfs/connected-client-maps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_ips",
            default=[],
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
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
    ),
)

model_registry.register_mapping("OntapNfsClientsMap", ONTAPNFSCLIENTSMAP_MAPPING)
