"""OntapFpolicyPersistentStore type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.fpolicy.persistent_stores.model import (
    OntapFpolicyPersistentStore,
)

ONTAPFPOLICYPERSISTENTSTORE_MAPPING = TypeMapping(
    name="OntapFpolicyPersistentStore",
    model_class=OntapFpolicyPersistentStore,
    api_endpoint="/protocols/fpolicy/{svm.uuid}/persistent-stores?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="autosize_mode",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="volume",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicyPersistentStore", ONTAPFPOLICYPERSISTENTSTORE_MAPPING)
