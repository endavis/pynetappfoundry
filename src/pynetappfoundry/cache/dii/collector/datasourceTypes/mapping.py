# ruff: noqa: N802
"""DiiCollectorDatasourceTypes type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.collector.datasourceTypes.model import (
    DiiCollectorDatasourceTypes,
    DiiCollectorDatasourceTypesPackage,
    DiiCollectorDatasourceTypesVendormodel,
)


def _transform_packages(record: dict[str, Any]) -> list[DiiCollectorDatasourceTypesPackage]:
    """Transform packages into DiiCollectorDatasourceTypesPackage list."""
    return [DiiCollectorDatasourceTypesPackage(**item) for item in record.get("packages", [])]


def _transform_vendorModels(record: dict[str, Any]) -> list[DiiCollectorDatasourceTypesVendormodel]:
    """Transform vendorModels into DiiCollectorDatasourceTypesVendormodel list."""
    return [
        DiiCollectorDatasourceTypesVendormodel(**item) for item in record.get("vendorModels", [])
    ]


DIICOLLECTORDATASOURCETYPES_MAPPING = TypeMapping(
    name="DiiCollectorDatasourceTypes",
    model_class=DiiCollectorDatasourceTypes,
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

model_registry.register_mapping("DiiCollectorDatasourceTypes", DIICOLLECTORDATASOURCETYPES_MAPPING)
