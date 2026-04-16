"""OntapIpsecPolicyResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.ipsec.policies.model import OntapIpsecPolicyResponse

ONTAPIPSECPOLICYRESPONSE_MAPPING = TypeMapping(
    name="OntapIpsecPolicyResponse",
    model_class=OntapIpsecPolicyResponse,
    api_endpoint="/security/ipsec/policies?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="action",
        ),
        FieldMapping(
            cache_attr="authentication_method",
        ),
        FieldMapping(
            cache_attr="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="local_endpoint.address",
        ),
        FieldMapping(
            cache_attr="local_endpoint.family",
        ),
        FieldMapping(
            cache_attr="local_endpoint.netmask",
        ),
        FieldMapping(
            cache_attr="local_endpoint.port",
        ),
        FieldMapping(
            cache_attr="local_identity",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="remote_endpoint.address",
        ),
        FieldMapping(
            cache_attr="remote_endpoint.family",
        ),
        FieldMapping(
            cache_attr="remote_endpoint.netmask",
        ),
        FieldMapping(
            cache_attr="remote_endpoint.port",
        ),
        FieldMapping(
            cache_attr="remote_identity",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="secret_key",
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
    ),
)

model_registry.register_mapping("OntapIpsecPolicyResponse", ONTAPIPSECPOLICYRESPONSE_MAPPING)
