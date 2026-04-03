"""OntapSvmPeerPermission type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.peer_permissions.model import OntapSvmPeerPermission

ONTAPSVMPEERPERMISSION_MAPPING = TypeMapping(
    name="OntapSvmPeerPermission",
    model_class=OntapSvmPeerPermission,
    api_endpoint="/svm/peer-permissions?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
        FieldMapping(
            cache_attr="cluster_peer.name",
        ),
        FieldMapping(
            cache_attr="cluster_peer.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmPeerPermission", ONTAPSVMPEERPERMISSION_MAPPING)
