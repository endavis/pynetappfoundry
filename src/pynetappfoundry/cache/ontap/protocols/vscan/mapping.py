"""OntapVscan type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.model import (
    OntapVscan,
    OntapVscanOnAccessPolicy,
    OntapVscanOnDemandPolicy,
    OntapVscanScannerPool,
)

ONTAPVSCAN_MAPPING = TypeMapping(
    name="OntapVscan",
    model_class=OntapVscan,
    api_endpoint="/protocols/vscan?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="cache_clear",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="on_access_policies",
            item_model=OntapVscanOnAccessPolicy,
            default=[],
        ),
        FieldMapping(
            cache_attr="on_demand_policies",
            item_model=OntapVscanOnDemandPolicy,
            default=[],
        ),
        FieldMapping(
            cache_attr="scanner_pools",
            item_model=OntapVscanScannerPool,
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

model_registry.register_mapping("OntapVscan", ONTAPVSCAN_MAPPING)
