"""DiiAssetsIscsinetworkportalsDevice type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.iSCSINetworkPortals.device.model import (
    DiiAssetsIscsinetworkportalsDevice,
)

DIIASSETSISCSINETWORKPORTALSDEVICE_MAPPING = TypeMapping(
    name="DiiAssetsIscsinetworkportalsDevice",
    model_class=DiiAssetsIscsinetworkportalsDevice,
    api_endpoint="/assets/iSCSINetworkPortals/{id}/device",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
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
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsIscsinetworkportalsDevice", DIIASSETSISCSINETWORKPORTALSDEVICE_MAPPING
)
