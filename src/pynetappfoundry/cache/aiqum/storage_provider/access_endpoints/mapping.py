"""AiqumAccessEndpoint type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.access_endpoints.model import AiqumAccessEndpoint

AIQUMACCESSENDPOINT_MAPPING = TypeMapping(
    name="AiqumAccessEndpoint",
    model_class=AiqumAccessEndpoint,
    api_endpoint="/storage-provider/access-endpoints",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="data_protocols",
            default=[],
        ),
        FieldMapping(
            cache_attr="fileshare.key",
        ),
        FieldMapping(
            cache_attr="gateway",
        ),
        FieldMapping(
            cache_attr="gateways",
            default=[],
        ),
        FieldMapping(
            cache_attr="ip.address",
        ),
        FieldMapping(
            cache_attr="ip.ha_address",
        ),
        FieldMapping(
            cache_attr="ip.netmask",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="lun.key",
        ),
        FieldMapping(
            cache_attr="mtu",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vlan",
            default=0,
        ),
        FieldMapping(
            cache_attr="wwpn",
        ),
    ),
)

model_registry.register_mapping("AiqumAccessEndpoint", AIQUMACCESSENDPOINT_MAPPING)
