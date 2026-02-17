"""OntapMediatorResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.mediators.model import OntapMediatorResponse
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

ONTAPMEDIATORRESPONSE_MAPPING = TypeMapping(
    name="OntapMediatorResponse",
    model_class=OntapMediatorResponse,
    api_endpoint="/cluster/mediators?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ca_certificate",
            api_path="ca_certificate",
        ),
        FieldMapping(
            cache_attr="dr_group_id",
            api_path="dr_group.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="ip_address",
            api_path="ip_address",
        ),
        FieldMapping(
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="peer_cluster_name",
            api_path="peer_cluster.name",
        ),
        FieldMapping(
            cache_attr="peer_cluster_uuid",
            api_path="peer_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="peer_mediator_connectivity",
            api_path="peer_mediator_connectivity",
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="reachable",
            api_path="reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="user",
            api_path="user",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMediatorResponse", ONTAPMEDIATORRESPONSE_MAPPING)
