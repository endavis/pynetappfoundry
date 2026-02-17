"""OntapIpsec type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.ipsec.model import OntapIpsec

ONTAPIPSEC_MAPPING = TypeMapping(
    name="OntapIpsec",
    model_class=OntapIpsec,
    api_endpoint="/security/ipsec?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="offload_enabled",
            api_path="offload_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="replay_window",
            api_path="replay_window",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapIpsec", ONTAPIPSEC_MAPPING)
