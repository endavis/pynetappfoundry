# ruff: noqa: N802
"""DiiCollectorDatasourcetype type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.collector.datasourceTypes.model import (
    DiiCollectorDatasourcetype,
    DiiCollectorDatasourcetypePackage,
    DiiCollectorDatasourcetypeVendormodel,
)


def _transform_packages(record: dict[str, Any]) -> list[DiiCollectorDatasourcetypePackage]:
    """Transform packages into DiiCollectorDatasourcetypePackage list."""
    return [DiiCollectorDatasourcetypePackage(**item) for item in record.get("packages", [])]


def _transform_vendorModels(record: dict[str, Any]) -> list[DiiCollectorDatasourcetypeVendormodel]:
    """Transform vendorModels into DiiCollectorDatasourcetypeVendormodel list."""
    return [
        DiiCollectorDatasourcetypeVendormodel(**item) for item in record.get("vendorModels", [])
    ]


DIICOLLECTORDATASOURCETYPE_MAPPING = TypeMapping(
    name="DiiCollectorDatasourcetype",
    model_class=DiiCollectorDatasourcetype,
    api_endpoint="/collector/datasourceTypes",
    api_type="dii",
    identifier_field="dataSourceTypeId",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="packages",
            transform=_transform_packages,
            default=[],
        ),
        FieldMapping(
            cache_attr="vendorModels",
            transform=_transform_vendorModels,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiCollectorDatasourcetype", DIICOLLECTORDATASOURCETYPE_MAPPING)
