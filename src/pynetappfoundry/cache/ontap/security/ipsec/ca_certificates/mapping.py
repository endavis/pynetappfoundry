"""OntapIpsecCaCertificate type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.ipsec.ca_certificates.model import (
    OntapIpsecCaCertificate,
)

ONTAPIPSECCACERTIFICATE_MAPPING = TypeMapping(
    name="OntapIpsecCaCertificate",
    model_class=OntapIpsecCaCertificate,
    api_endpoint="/security/ipsec/ca-certificates?fields=*",
    api_type="ontap",
    identifier_field="certificate.uuid",
    fields=(
        FieldMapping(
            cache_attr="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpsecCaCertificate", ONTAPIPSECCACERTIFICATE_MAPPING)
