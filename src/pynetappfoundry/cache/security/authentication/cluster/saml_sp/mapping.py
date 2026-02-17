"""OntapSecuritySamlSp type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.authentication.cluster.saml_sp.model import OntapSecuritySamlSp

ONTAPSECURITYSAMLSP_MAPPING = TypeMapping(
    name="OntapSecuritySamlSp",
    model_class=OntapSecuritySamlSp,
    api_endpoint="/security/authentication/cluster/saml-sp?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="certificate_ca",
            api_path="certificate.ca",
        ),
        FieldMapping(
            cache_attr="certificate_common_name",
            api_path="certificate.common_name",
        ),
        FieldMapping(
            cache_attr="certificate_serial_number",
            api_path="certificate.serial_number",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="host",
            api_path="host",
        ),
        FieldMapping(
            cache_attr="idp_uri",
            api_path="idp_uri",
        ),
    ),
)

model_registry.register_mapping("OntapSecuritySamlSp", ONTAPSECURITYSAMLSP_MAPPING)
