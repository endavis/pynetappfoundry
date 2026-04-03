"""OntapFabric type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.fabrics.model import OntapFabric

ONTAPFABRIC_MAPPING = TypeMapping(
    name="OntapFabric",
    model_class=OntapFabric,
    api_endpoint="/network/fc/fabrics?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cache.age",
        ),
        FieldMapping(
            cache_attr="cache.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="cache.update_time",
        ),
        FieldMapping(
            cache_attr="connections",
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="zoneset.name",
        ),
    ),
)

model_registry.register_mapping("OntapFabric", ONTAPFABRIC_MAPPING)
