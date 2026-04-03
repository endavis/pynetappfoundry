"""OntapSecuritySamlSp type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.cluster.saml_sp.model import (
    OntapSecuritySamlSp,
)

ONTAPSECURITYSAMLSP_MAPPING = TypeMapping(
    name="OntapSecuritySamlSp",
    model_class=OntapSecuritySamlSp,
    api_endpoint="/security/authentication/cluster/saml-sp?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="certificate.ca",
        ),
        FieldMapping(
            cache_attr="certificate.common_name",
        ),
        FieldMapping(
            cache_attr="certificate.serial_number",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="host",
        ),
        FieldMapping(
            cache_attr="idp_uri",
        ),
    ),
)

model_registry.register_mapping("OntapSecuritySamlSp", ONTAPSECURITYSAMLSP_MAPPING)
