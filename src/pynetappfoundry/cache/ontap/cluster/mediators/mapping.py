"""OntapMediatorResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse

ONTAPMEDIATORRESPONSE_MAPPING = TypeMapping(
    name="OntapMediatorResponse",
    model_class=OntapMediatorResponse,
    api_endpoint="/cluster/mediators?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ca_certificate",
        ),
        FieldMapping(
            cache_attr="dr_group.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="ip_address",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="peer_cluster.name",
        ),
        FieldMapping(
            cache_attr="peer_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="peer_mediator_connectivity",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="user",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMediatorResponse", ONTAPMEDIATORRESPONSE_MAPPING)
