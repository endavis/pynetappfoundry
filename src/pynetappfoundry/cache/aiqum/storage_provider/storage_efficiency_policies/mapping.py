"""AiqumStorageEfficiencyPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.storage_efficiency_policies.model import (
    AiqumStorageEfficiencyPolicy,
)

AIQUMSTORAGEEFFICIENCYPOLICY_MAPPING = TypeMapping(
    name="AiqumStorageEfficiencyPolicy",
    model_class=AiqumStorageEfficiencyPolicy,
    api_endpoint="/storage-provider/storage-efficiency-policies",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="compression",
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="deduplication",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="space_thin_provisioned",
            default=False,
        ),
        FieldMapping(
            cache_attr="system_defined",
            default=False,
        ),
        FieldMapping(
            cache_attr="update_time",
        ),
        FieldMapping(
            cache_attr="workload_count",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "AiqumStorageEfficiencyPolicy", AIQUMSTORAGEEFFICIENCYPOLICY_MAPPING
)
