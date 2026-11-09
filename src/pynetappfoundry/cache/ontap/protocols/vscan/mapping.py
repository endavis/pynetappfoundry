"""OntapVscan type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.model import (
    OntapVscan,
    OntapVscanOnAccessPolicy,
    OntapVscanOnDemandPolicy,
    OntapVscanScannerPool,
)


def _transform_on_access_policies(record: dict[str, Any]) -> list[OntapVscanOnAccessPolicy]:
    """Transform on_access_policies into OntapVscanOnAccessPolicy list."""
    return [OntapVscanOnAccessPolicy(**item) for item in record.get("on_access_policies", [])]


def _transform_on_demand_policies(record: dict[str, Any]) -> list[OntapVscanOnDemandPolicy]:
    """Transform on_demand_policies into OntapVscanOnDemandPolicy list."""
    return [OntapVscanOnDemandPolicy(**item) for item in record.get("on_demand_policies", [])]


def _transform_scanner_pools(record: dict[str, Any]) -> list[OntapVscanScannerPool]:
    """Transform scanner_pools into OntapVscanScannerPool list."""
    return [OntapVscanScannerPool(**item) for item in record.get("scanner_pools", [])]


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
            transform=_transform_on_access_policies,
            default=[],
        ),
        FieldMapping(
            cache_attr="on_demand_policies",
            transform=_transform_on_demand_policies,
            default=[],
        ),
        FieldMapping(
            cache_attr="scanner_pools",
            transform=_transform_scanner_pools,
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
