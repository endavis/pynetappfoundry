"""AiqumActiveDirectoryMappings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.active_directories_mappings.model import (
    AiqumActiveDirectoryMappings,
)

AIQUMACTIVEDIRECTORYMAPPINGS_MAPPING = TypeMapping(
    name="AiqumActiveDirectoryMappings",
    model_class=AiqumActiveDirectoryMappings,
    api_endpoint="/storage-provider/active-directories-mappings",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="dns",
        ),
        FieldMapping(
            cache_attr="domain",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="username",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumActiveDirectoryMappings", AIQUMACTIVEDIRECTORYMAPPINGS_MAPPING
)
