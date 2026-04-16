"""DiiAssetsGenericdevice type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.genericDevices.model import DiiAssetsGenericdevice

DIIASSETSGENERICDEVICE_MAPPING = TypeMapping(
    name="DiiAssetsGenericdevice",
    model_class=DiiAssetsGenericdevice,
    api_endpoint="/assets/genericDevices",
    api_type="dii",
    identifier_field="id",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="fcPortCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="zones",
            default=[],
        ),
        FieldMapping(
            cache_attr="isActive",
            default=False,
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsGenericdevice", DIIASSETSGENERICDEVICE_MAPPING)
