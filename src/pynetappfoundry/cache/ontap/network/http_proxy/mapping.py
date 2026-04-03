"""OntapNetworkHttpProxy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.http_proxy.model import OntapNetworkHttpProxy

ONTAPNETWORKHTTPPROXY_MAPPING = TypeMapping(
    name="OntapNetworkHttpProxy",
    model_class=OntapNetworkHttpProxy,
    api_endpoint="/network/http-proxy?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="server",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="username",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNetworkHttpProxy", ONTAPNETWORKHTTPPROXY_MAPPING)
