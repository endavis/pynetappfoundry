"""OntapIpsecCaCertificate type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.ipsec.ca_certificates.model import OntapIpsecCaCertificate

ONTAPIPSECCACERTIFICATE_MAPPING = TypeMapping(
    name="OntapIpsecCaCertificate",
    model_class=OntapIpsecCaCertificate,
    api_endpoint="/security/ipsec/ca-certificates?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="certificate_uuid",
            api_path="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpsecCaCertificate", ONTAPIPSECCACERTIFICATE_MAPPING)
