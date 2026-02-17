"""OntapSecurityOauth2Global type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.authentication.cluster.oauth2.model import (
    OntapSecurityOauth2Global,
)

ONTAPSECURITYOAUTH2GLOBAL_MAPPING = TypeMapping(
    name="OntapSecurityOauth2Global",
    model_class=OntapSecurityOauth2Global,
    api_endpoint="/security/authentication/cluster/oauth2?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSecurityOauth2Global", ONTAPSECURITYOAUTH2GLOBAL_MAPPING)
