"""OntapAutoUpdateConfiguration type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.auto_update.configurations.model import (
    OntapAutoUpdateConfiguration,
)

ONTAPAUTOUPDATECONFIGURATION_MAPPING = TypeMapping(
    name="OntapAutoUpdateConfiguration",
    model_class=OntapAutoUpdateConfiguration,
    api_endpoint="/support/auto-update/configurations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="action",
            api_path="action",
        ),
        FieldMapping(
            cache_attr="category",
            api_path="category",
        ),
        FieldMapping(
            cache_attr="description_code",
            api_path="description.code",
        ),
        FieldMapping(
            cache_attr="description_message",
            api_path="description.message",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapAutoUpdateConfiguration", ONTAPAUTOUPDATECONFIGURATION_MAPPING
)
