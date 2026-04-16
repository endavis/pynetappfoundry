"""OntapVscanScannerPool type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.scanner_pools.model import OntapVscanScannerPool

ONTAPVSCANSCANNERPOOL_MAPPING = TypeMapping(
    name="OntapVscanScannerPool",
    model_class=OntapVscanScannerPool,
    api_endpoint="/protocols/vscan/{svm.uuid}/scanner-pools?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="privileged_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="role",
        ),
        FieldMapping(
            cache_attr="servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVscanScannerPool", ONTAPVSCANSCANNERPOOL_MAPPING)
