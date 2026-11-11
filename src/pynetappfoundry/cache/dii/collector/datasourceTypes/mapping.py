"""DiiCollectorDatasourceTypes type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.collector.datasourceTypes.model import (
    DiiCollectorDatasourceTypes,
    DiiCollectorDatasourceTypesPackage,
    DiiCollectorDatasourceTypesVendormodel,
)

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
            item_model=DiiCollectorDatasourceTypesPackage,
            default=[],
        ),
        FieldMapping(
            cache_attr="vendorModels",
            item_model=DiiCollectorDatasourceTypesVendormodel,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiCollectorDatasourceTypes", DIICOLLECTORDATASOURCETYPES_MAPPING)
