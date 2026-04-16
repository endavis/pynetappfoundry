"""DiiIscsinetworkportal type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.iSCSINetworkPortals.model import DiiIscsinetworkportal

DIIISCSINETWORKPORTAL_MAPPING = TypeMapping(
    name="DiiIscsinetworkportal",
    model_class=DiiIscsinetworkportal,
    api_endpoint="/assets/iSCSINetworkPortals/{id}",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="nicName",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="port",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="portalGroupTag",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="device",
        ),
        FieldMapping(
            cache_attr="portalGroup",
        ),
    ),
)

model_registry.register_mapping("DiiIscsinetworkportal", DIIISCSINETWORKPORTAL_MAPPING)
