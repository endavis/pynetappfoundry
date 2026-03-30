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
            api_path="applications",
            default=[],
        ),
        FieldMapping(
            cache_attr="cluster_peer_name",
            api_path="cluster_peer.name",
        ),
        FieldMapping(
            cache_attr="cluster_peer_uuid",
            api_path="cluster_peer.uuid",
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

model_registry.register_mapping("OntapSvmPeerPermission", ONTAPSVMPEERPERMISSION_MAPPING)
