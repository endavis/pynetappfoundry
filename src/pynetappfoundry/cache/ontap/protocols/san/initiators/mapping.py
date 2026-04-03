"""OntapInitiator type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.initiators.model import OntapInitiator

ONTAPINITIATOR_MAPPING = TypeMapping(
    name="OntapInitiator",
    model_class=OntapInitiator,
    api_endpoint="/protocols/san/initiators?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapInitiator", ONTAPINITIATOR_MAPPING)
