"""OntapVscanScannerPool type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.vscan.scanner_pools.model import OntapVscanScannerPool

ONTAPVSCANSCANNERPOOL_MAPPING = TypeMapping(
    name="OntapVscanScannerPool",
    model_class=OntapVscanScannerPool,
    api_endpoint="/protocols/vscan/{svm.uuid}/scanner-pools?fields=*",
    api_type="ontap",
    parent_mapping="OntapProtocolsVscan",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="cluster_name",
            api_path="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster_uuid",
            api_path="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="privileged_users",
            api_path="privileged_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="role",
            api_path="role",
        ),
        FieldMapping(
            cache_attr="servers",
            api_path="servers",
            default=[],
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

model_registry.register_mapping("OntapVscanScannerPool", ONTAPVSCANSCANNERPOOL_MAPPING)
