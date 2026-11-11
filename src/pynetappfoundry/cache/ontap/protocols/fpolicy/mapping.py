"""OntapFpolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.fpolicy.model import (
    OntapFpolicy,
    OntapFpolicyEngine,
    OntapFpolicyEvent,
    OntapFpolicyPersistentStore,
    OntapFpolicyPolicy,
)

ONTAPFPOLICY_MAPPING = TypeMapping(
    name="OntapFpolicy",
    model_class=OntapFpolicy,
    api_endpoint="/protocols/fpolicy?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="engines",
            item_model=OntapFpolicyEngine,
            default=[],
        ),
        FieldMapping(
            cache_attr="events",
            item_model=OntapFpolicyEvent,
            default=[],
        ),
        FieldMapping(
            cache_attr="persistent_stores",
            item_model=OntapFpolicyPersistentStore,
            default=[],
        ),
        FieldMapping(
            cache_attr="policies",
            item_model=OntapFpolicyPolicy,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicy", ONTAPFPOLICY_MAPPING)
