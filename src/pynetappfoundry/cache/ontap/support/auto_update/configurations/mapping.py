"""OntapAutoUpdateConfiguration type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.auto_update.configurations.model import (
    OntapAutoUpdateConfiguration,
)

ONTAPAUTOUPDATECONFIGURATION_MAPPING = TypeMapping(
    name="OntapAutoUpdateConfiguration",
    model_class=OntapAutoUpdateConfiguration,
    api_endpoint="/support/auto-update/configurations?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="action",
        ),
        FieldMapping(
            cache_attr="category",
        ),
        FieldMapping(
            cache_attr="description.code",
        ),
        FieldMapping(
            cache_attr="description.message",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapAutoUpdateConfiguration", ONTAPAUTOUPDATECONFIGURATION_MAPPING
)
