"""OntapClusterNdmpProperties type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.ndmp.model import OntapClusterNdmpProperties

ONTAPCLUSTERNDMPPROPERTIES_MAPPING = TypeMapping(
    name="OntapClusterNdmpProperties",
    model_class=OntapClusterNdmpProperties,
    api_endpoint="/protocols/ndmp?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="mode",
            api_path="mode",
        ),
    ),
)

model_registry.register_mapping("OntapClusterNdmpProperties", ONTAPCLUSTERNDMPPROPERTIES_MAPPING)
