"""OntapSvmPeer type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.peers.model import OntapSvmPeer

ONTAPSVMPEER_MAPPING = TypeMapping(
    name="OntapSvmPeer",
    model_class=OntapSvmPeer,
    api_endpoint="/svm/peers?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
        FieldMapping(
            cache_attr="force",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="peer.cluster.name",
        ),
        FieldMapping(
            cache_attr="peer.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="peer.svm.name",
        ),
        FieldMapping(
            cache_attr="peer.svm.uuid",
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
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmPeer", ONTAPSVMPEER_MAPPING)
