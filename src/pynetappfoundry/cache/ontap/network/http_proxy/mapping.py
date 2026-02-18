"""OntapNetworkHttpProxy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.http_proxy.model import OntapNetworkHttpProxy

ONTAPNETWORKHTTPPROXY_MAPPING = TypeMapping(
    name="OntapNetworkHttpProxy",
    model_class=OntapNetworkHttpProxy,
    api_endpoint="/network/http-proxy?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_enabled",
            api_path="authentication_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ipspace_name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace_uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="server",
            api_path="server",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="username",
            api_path="username",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNetworkHttpProxy", ONTAPNETWORKHTTPPROXY_MAPPING)
