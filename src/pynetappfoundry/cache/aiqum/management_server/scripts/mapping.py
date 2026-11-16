"""AiqumScript type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.management_server.scripts.model import AiqumScript

AIQUMSCRIPT_MAPPING = TypeMapping(
    name="AiqumScript",
    model_class=AiqumScript,
    api_endpoint="/management-server/scripts",
    api_type="aiqum",
    fields=(
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
    ),
)

model_registry.register_mapping("AiqumScript", AIQUMSCRIPT_MAPPING)
