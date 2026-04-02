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
    fields=(
        FieldMapping(
            cache_attr="applications",
            api_path="applications",
            default=[],
        ),
        FieldMapping(
            cache_attr="force",
            api_path="force",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="peer.cluster.name",
            api_path="peer.cluster.name",
        ),
        FieldMapping(
            cache_attr="peer.cluster.uuid",
            api_path="peer.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="peer.svm.name",
            api_path="peer.svm.name",
        ),
        FieldMapping(
            cache_attr="peer.svm.uuid",
            api_path="peer.svm.uuid",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmPeer", ONTAPSVMPEER_MAPPING)
