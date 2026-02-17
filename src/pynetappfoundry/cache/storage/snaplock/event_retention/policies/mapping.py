"""OntapSnaplockRetentionPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.storage.snaplock.event_retention.policies.model import (
    OntapSnaplockRetentionPolicy,
)

ONTAPSNAPLOCKRETENTIONPOLICY_MAPPING = TypeMapping(
    name="OntapSnaplockRetentionPolicy",
    model_class=OntapSnaplockRetentionPolicy,
    api_endpoint="/storage/snaplock/event-retention/policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="retention_period",
            api_path="retention_period",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapSnaplockRetentionPolicy", ONTAPSNAPLOCKRETENTIONPOLICY_MAPPING
)
