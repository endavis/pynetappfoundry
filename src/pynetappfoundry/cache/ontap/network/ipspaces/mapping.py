"""OntapIpspace type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.ipspaces.model import OntapIpspace

ONTAPIPSPACE_MAPPING = TypeMapping(
    name="OntapIpspace",
    model_class=OntapIpspace,
    api_endpoint="/network/ipspaces?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpspace", ONTAPIPSPACE_MAPPING)
