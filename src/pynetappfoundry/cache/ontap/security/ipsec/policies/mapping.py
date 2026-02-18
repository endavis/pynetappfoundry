"""OntapIpsecPolicyResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.ipsec.policies.model import OntapIpsecPolicyResponse

ONTAPIPSECPOLICYRESPONSE_MAPPING = TypeMapping(
    name="OntapIpsecPolicyResponse",
    model_class=OntapIpsecPolicyResponse,
    api_endpoint="/security/ipsec/policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="action",
            api_path="action",
        ),
        FieldMapping(
            cache_attr="authentication_method",
            api_path="authentication_method",
        ),
        FieldMapping(
            cache_attr="certificate_name",
            api_path="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate_uuid",
            api_path="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
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
            cache_attr="local_endpoint_address",
            api_path="local_endpoint.address",
        ),
        FieldMapping(
            cache_attr="local_endpoint_family",
            api_path="local_endpoint.family",
        ),
        FieldMapping(
            cache_attr="local_endpoint_netmask",
            api_path="local_endpoint.netmask",
        ),
        FieldMapping(
            cache_attr="local_endpoint_port",
            api_path="local_endpoint.port",
        ),
        FieldMapping(
            cache_attr="local_identity",
            api_path="local_identity",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="remote_endpoint_address",
            api_path="remote_endpoint.address",
        ),
        FieldMapping(
            cache_attr="remote_endpoint_family",
            api_path="remote_endpoint.family",
        ),
        FieldMapping(
            cache_attr="remote_endpoint_netmask",
            api_path="remote_endpoint.netmask",
        ),
        FieldMapping(
            cache_attr="remote_endpoint_port",
            api_path="remote_endpoint.port",
        ),
        FieldMapping(
            cache_attr="remote_identity",
            api_path="remote_identity",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="secret_key",
            api_path="secret_key",
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
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpsecPolicyResponse", ONTAPIPSECPOLICYRESPONSE_MAPPING)
