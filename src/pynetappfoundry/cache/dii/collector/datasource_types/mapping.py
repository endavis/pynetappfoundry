"""DiiCollectorDatasourceType type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.collector.datasource_types.model import (
    DiiCollectorDatasourceType,
    DiiCollectorDatasourceTypePackage,
    DiiCollectorDatasourceTypeVendormodel,
)

DIICOLLECTORDATASOURCETYPE_MAPPING = TypeMapping(
    name="DiiCollectorDatasourceType",
    model_class=DiiCollectorDatasourceType,
    api_endpoint="/collector/datasource_types",
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
            item_model=DiiCollectorDatasourceTypePackage,
            default=[],
        ),
        FieldMapping(
            cache_attr="vendorModels",
            item_model=DiiCollectorDatasourceTypeVendormodel,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiCollectorDatasourceType", DIICOLLECTORDATASOURCETYPE_MAPPING)
